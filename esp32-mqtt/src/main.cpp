/**********************************************************************************
 * Blue Star AC -> ESP32 DevKit V1 -> HiveMQ Cloud (MQTT + TLS) -> Vercel Dashboard
 * 
 * Hardware:
 *   ESP32 DevKit V1
 *   Blue Star AC Display Board 4-pin Wi-Fi port (Megmeet MD50BS or equivalent)
 * 
 * Pinout:
 *   AC 5V      -> ESP32 VIN (5V)
 *   AC GND     -> ESP32 GND
 *   AC R_WIFI  -> 5k ohm in series -> ESP32 GPIO 16 (RX2)
 *                 10k ohm resistor from GPIO 16 to GND (Voltage Divider: 5V -> ~3.3V)
 *   AC T_WIFI  -> ESP32 GPIO 17 (TX2) direct
 **********************************************************************************/

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <ArduinoOTA.h>
#include <vector>
#include <deque>

#if __has_include("secrets.h")
  #include "secrets.h"
#else
  #include "secrets.example.h"
#endif

// ==================== 1. WI-FI & ADAFRUIT IO CREDENTIALS ====================
const char* ssid = WIFI_SSID;
const char* pass = WIFI_PASS;

// Adafruit IO Broker details
const char* mqtt_server   = "io.adafruit.com";
const int   mqtt_port     = 8883; // Secure TLS port
const char* mqtt_user     = AIO_USERNAME;
const char* mqtt_password = AIO_KEY;

// Adafruit IO Topics
String topicStatusStr = String(AIO_USERNAME) + "/feeds/bluestar-ac-status";
String topicSetStr    = String(AIO_USERNAME) + "/feeds/bluestar-ac-set";
#define TOPIC_STATUS  topicStatusStr.c_str()
#define TOPIC_SET     topicSetStr.c_str()

// ==================== 2. UART CONFIGURATION ====================
#define AC_RX_PIN 16  // Connects to AC R_WIFI (via voltage divider)
#define AC_TX_PIN 17  // Connects to AC T_WIFI
HardwareSerial acSerial(2);

// ==================== 3. TUYA PROTOCOL CONSTANTS ====================
static const uint8_t CMD_HEARTBEAT     = 0x00;
static const uint8_t CMD_PRODUCT_QUERY = 0x01;
static const uint8_t CMD_WORKING_MODE  = 0x02;
static const uint8_t CMD_NET_STATUS    = 0x03;
static const uint8_t CMD_DP_SET        = 0x06;
static const uint8_t CMD_DP_REPORT     = 0x07;
static const uint8_t CMD_QUERY_ALL     = 0x08;

static const uint8_t NET_STATUS_CLOUD  = 0x04;
static const uint8_t DP_RECORD         = 101;  // Blue Star string DP

static const uint32_t TX_SPACING_MS    = 400;  // AC drops frames if sent faster
static const uint32_t RX_TIMEOUT_MS    = 300;
static const uint32_t SILENCE_REHANDSHAKE_MS = 180000;

// Internal AC state
bool acPower = false;
float targetTemp = 24.0;
int acMode = 2; // 2 = Cool
int acFan = 7;  // 7 = Auto
int acVane = 6; // 6 = Off, 0 = Swing
int hSwing = 6; // 6 = Off, 0 = Swing
int convertible = 1; // 1 = 100%
bool ecoMode = false;
bool turboCool = false;
bool comfortSleep = false;
bool displayLight = true;
bool buzzerMute = false;
bool filterAlert = false;
float roomTemp = 0.0;
float acRunHours = 0.0;
float compRunHours = 0.0;
long compressorHz = 0;
float coilTemp = 0.0;

uint32_t lastTxTime = 0;
uint32_t lastRxByteTime = 0;
uint32_t lastValidFrameTime = 0;
uint32_t lastMqttPublishTime = 0;
uint32_t lastHeartbeatTime = 0;
uint32_t lastMqttReconnectTime = 0;

std::vector<uint8_t> rxBuffer;
std::deque<std::vector<uint8_t>> txQueue;

WiFiClientSecure espClient;
PubSubClient mqttClient(espClient);
WiFiServer telnetServer(23);
WiFiClient telnetClient;

void dbgPrint(const String &str) {
  Serial.print(str);
  if (telnetClient && telnetClient.connected()) {
    telnetClient.print(str);
  }
}

void dbgPrintf(const char *format, ...) {
  char buf[256];
  va_list args;
  va_start(args, format);
  vsnprintf(buf, sizeof(buf), format, args);
  va_end(args);
  dbgPrint(buf);
}

void dbgPrintln(const String &str = "") {
  dbgPrint(str + "\n");
}

// ==================== 4. CRC-16 / MODBUS ====================
uint16_t crc16_modbus(const char *data, size_t len) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < len; i++) {
    crc ^= static_cast<uint8_t>(data[i]);
    for (int b = 0; b < 8; b++) {
      crc = (crc & 1) ? (crc >> 1) ^ 0xA001 : crc >> 1;
    }
  }
  return crc;
}

// Queue raw Tuya frame
void queueTuyaFrame(uint8_t cmd, const std::vector<uint8_t> &payload = {}) {
  std::vector<uint8_t> frame = {
    0x55, 0xAA, 0x00, cmd,
    static_cast<uint8_t>(payload.size() >> 8),
    static_cast<uint8_t>(payload.size() & 0xFF)
  };
  frame.insert(frame.end(), payload.begin(), payload.end());
  uint8_t sum = 0;
  for (uint8_t b : frame) sum += b;
  frame.push_back(sum);
  txQueue.push_back(std::move(frame));
}

// Send Blue Star DP101 record: *LLKKV...CCCC#
void sendBlueStarRecord(const String &key, const String &value) {
  String inner = key + value;
  char lenHex[3];
  snprintf(lenHex, sizeof(lenHex), "%02X", (unsigned int)inner.length());
  String header = "*" + String(lenHex) + inner;
  
  uint16_t crc = crc16_modbus(header.c_str(), header.length());
  char crcHex[5];
  snprintf(crcHex, sizeof(crcHex), "%04X", crc);
  String fullRecord = header + String(crcHex) + "#";
  
  std::vector<uint8_t> payload;
  payload.push_back(DP_RECORD);
  payload.push_back(0x03); // String type
  payload.push_back(fullRecord.length() >> 8);
  payload.push_back(fullRecord.length() & 0xFF);
  for (size_t i = 0; i < fullRecord.length(); i++) {
    payload.push_back(static_cast<uint8_t>(fullRecord[i]));
  }
  
  dbgPrintf("[AC TX] Sending Record: %s\n", fullRecord.c_str());
  queueTuyaFrame(CMD_DP_SET, payload);
}

// Handshake
void sendHandshake() {
  dbgPrintln("[AC] >>> Sending Tuya Handshake to AC...");
  queueTuyaFrame(CMD_PRODUCT_QUERY);
  queueTuyaFrame(CMD_WORKING_MODE);
  queueTuyaFrame(CMD_NET_STATUS, {NET_STATUS_CLOUD});
  queueTuyaFrame(CMD_QUERY_ALL);
  queueTuyaFrame(CMD_HEARTBEAT);
  sendBlueStarRecord("00", "0"); // Query full state
}

// Publish AC state to HiveMQ as JSON
void publishState() {
  if (!mqttClient.connected()) return;

  JsonDocument doc;
  doc["power"]        = acPower ? 1 : 0;
  doc["targetTemp"]   = serialized(String(targetTemp, 1));
  doc["roomTemp"]     = serialized(String(roomTemp, 1));
  
  // Mode mapping: 1=Cool, 2=Dry, 3=Fan, 4=Auto
  int m = 1;
  if (acMode == 2) m = 1;
  else if (acMode == 3) m = 2;
  else if (acMode == 0) m = 3;
  else if (acMode == 4) m = 4;
  doc["mode"]         = m;

  // Fan mapping: 1=Quiet, 2=Low, 3=Med, 4=High, 5=Turbo, 6=Auto
  int f = 6;
  if (acFan == 1) f = 1;
  else if (acFan == 2) f = 2;
  else if (acFan == 3) f = 3;
  else if (acFan == 4) f = 4;
  else if (acFan == 6) f = 5;
  else if (acFan == 7) f = 6;
  doc["fan"]          = f;

  doc["vane"]         = acVane;
  doc["hSwing"]       = (hSwing == 0) ? 1 : 0;
  doc["convertible"]  = convertible;
  doc["eco"]          = ecoMode ? 1 : 0;
  doc["turbo"]        = turboCool ? 1 : 0;
  doc["sleep"]        = comfortSleep ? 1 : 0;
  doc["light"]        = displayLight ? 1 : 0;
  doc["mute"]         = buzzerMute ? 1 : 0;
  doc["filterAlert"]  = filterAlert ? 1 : 0;
  doc["compHz"]       = acPower ? compressorHz : 0;
  doc["coilTemp"]     = serialized(String(coilTemp, 1));
  doc["acHours"]      = serialized(String(acRunHours, 1));
  doc["compHours"]    = serialized(String(compRunHours, 1));
  doc["online"]       = true;

  char buffer[512];
  size_t n = serializeJson(doc, buffer);
  mqttClient.publish(TOPIC_STATUS, (const uint8_t*)buffer, n, true); // Retain flag true
  dbgPrintf("[MQTT TX] Published State: %s\n", buffer);
  lastMqttPublishTime = millis();
}

// Process incoming AC records
void handleBlueStarKey(const String &key, const String &value) {
  dbgPrintf("[AC RX DECODED] Key: %s | Value: %s\n", key.c_str(), value.c_str());
  bool stateChanged = false;

  if (key == "01") {
    acPower = (value == "1");
    stateChanged = true;
  }
  else if (key == "02") {
    long raw = strtol(value.c_str(), nullptr, 16);
    targetTemp = raw / 10.0f;
    stateChanged = true;
  }
  else if (key == "03") {
    acMode = value.toInt();
    stateChanged = true;
  }
  else if (key == "04") {
    acFan = value.toInt();
    stateChanged = true;
  }
  else if (key == "05") {
    acVane = value.toInt();
    stateChanged = true;
  }
  else if (key == "06") {
    hSwing = value.toInt();
    stateChanged = true;
  }
  else if (key == "55") {
    convertible = value.toInt();
    stateChanged = true;
  }
  else if (key == "15") {
    displayLight = (value == "1");
    stateChanged = true;
  }
  else if (key == "22") {
    ecoMode = (value == "1");
    stateChanged = true;
  }
  else if (key == "07") {
    turboCool = (value == "3");
    stateChanged = true;
  }
  else if (key == "11") {
    comfortSleep = (value == "1");
    stateChanged = true;
  }
  else if (key == "58") {
    buzzerMute = (value == "1");
    stateChanged = true;
  }
  else if (key == "24") { // Compressor Inverter Speed (Hz)
    if (value.length() >= 2) {
      compressorHz = strtol(value.substring(0, 2).c_str(), nullptr, 16);
      stateChanged = true;
    }
  }
  else if (key == "62") { // Coil Temperature
    long raw = strtol(value.c_str(), nullptr, 16);
    coilTemp = raw / 10.0f;
    stateChanged = true;
  }
  else if (key == "44") {
    long raw = strtol(value.c_str(), nullptr, 16);
    acRunHours = raw / 4.0f;
    stateChanged = true;
  }
  else if (key == "43") {
    long raw = strtol(value.c_str(), nullptr, 16);
    compRunHours = raw / 4.0f;
    stateChanged = true;
  }
  else if (key == "99") {
    long raw = strtol(value.c_str(), nullptr, 16);
    roomTemp = raw / 10.0f;
    stateChanged = true;
  }
  else if (key == "00") { // Full State Dump
    if (value.length() >= 34) {
      acPower = (value.charAt(0) == '1');
      targetTemp = strtol(value.substring(1, 4).c_str(), nullptr, 16) / 10.0f;
      acMode = value.substring(4, 5).toInt();
      acFan = value.substring(5, 6).toInt();
      acVane = value.substring(6, 7).toInt();
      hSwing = value.substring(7, 8).toInt();
      displayLight = (value.charAt(23) == '1');
      roomTemp = strtol(value.substring(31, 34).c_str(), nullptr, 16) / 10.0f;
      if (value.length() >= 51) {
        compRunHours = strtol(value.substring(39, 43).c_str(), nullptr, 16) / 4.0f;
        acRunHours = strtol(value.substring(43, 51).c_str(), nullptr, 16) / 4.0f;
      }
      if (value.length() > 103) {
        filterAlert = (value.charAt(103) == '1');
      }
      stateChanged = true;
    }
  }

  if (stateChanged) {
    publishState();
  }
}

// Parse string records: *LLKKV...CCCC#
void parseBlueStarRecord(const String &rec) {
  if (!rec.startsWith("*") || !rec.endsWith("#") || rec.length() < 9) return;
  
  dbgPrintf("[AC RX STR] %s\n", rec.c_str());
  String body = rec.substring(0, rec.length() - 5);
  String crcExpectedStr = rec.substring(rec.length() - 5, rec.length() - 1);
  uint16_t crcCalc = crc16_modbus(body.c_str(), body.length());
  char crcBuf[5];
  snprintf(crcBuf, sizeof(crcBuf), "%04X", crcCalc);
  if (crcExpectedStr != String(crcBuf)) {
    dbgPrintln("[AC WARN] CRC mismatch!");
    return;
  }
  
  String key = body.substring(3, 5);
  String val = body.substring(5);
  handleBlueStarKey(key, val);
}

// Parse Tuya DP payloads
void handleTuyaDatapoints(const uint8_t *data, size_t len) {
  size_t idx = 0;
  while (idx + 4 <= len) {
    uint8_t dpId = data[idx++];
    uint8_t dpType = data[idx++];
    uint16_t dpLen = (data[idx] << 8) | data[idx + 1];
    idx += 2;
    if (idx + dpLen > len) break;
    
    if (dpId == DP_RECORD && dpType == 0x03) {
      String rec = "";
      for (size_t i = 0; i < dpLen; i++) rec += (char)data[idx + i];
      parseBlueStarRecord(rec);
    }
    idx += dpLen;
  }
}

// Handle complete Tuya frame
void handleTuyaFrame(uint8_t cmd, const uint8_t *payload, size_t len) {
  lastValidFrameTime = millis();
  if (cmd == CMD_DP_REPORT || cmd == CMD_DP_SET) {
    handleTuyaDatapoints(payload, len);
  } else if (cmd == CMD_HEARTBEAT) {
    if (len > 0 && payload[0] == 0x00) {
      Serial.println("[AC] MCU reported restart, re-handshaking...");
      sendHandshake();
    }
  }
}

// Serial Receiver
void processIncomingSerial() {
  while (acSerial.available()) {
    uint8_t b = acSerial.read();
    uint32_t now = millis();
    if (!rxBuffer.empty() && now - lastRxByteTime > RX_TIMEOUT_MS) {
      rxBuffer.clear();
    }
    lastRxByteTime = now;
    
    rxBuffer.push_back(b);
    if (rxBuffer.size() < 2) continue;
    if (rxBuffer[0] != 0x55 || rxBuffer[1] != 0xAA) {
      rxBuffer.erase(rxBuffer.begin());
      continue;
    }
    if (rxBuffer.size() < 6) continue;
    
    uint16_t payloadLen = (rxBuffer[4] << 8) | rxBuffer[5];
    size_t frameLen = 6 + payloadLen + 1;
    if (rxBuffer.size() < frameLen) continue;
    
    uint8_t sum = 0;
    for (size_t i = 0; i < frameLen - 1; i++) sum += rxBuffer[i];
    if (sum == rxBuffer[frameLen - 1]) {
      handleTuyaFrame(rxBuffer[3], &rxBuffer[6], payloadLen);
    }
    rxBuffer.erase(rxBuffer.begin(), rxBuffer.begin() + frameLen);
  }
}

// Serial Transmitter
void processTxQueue() {
  if (!txQueue.empty() && millis() - lastTxTime >= TX_SPACING_MS && rxBuffer.empty()) {
    auto &frame = txQueue.front();
    acSerial.write(frame.data(), frame.size());
    acSerial.flush();
    lastTxTime = millis();
    txQueue.pop_front();
  }
}

// ==================== 5. MQTT CALLBACK (INCOMING COMMANDS FROM VERCEL) ====================
void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  char jsonBuf[512];
  if (length >= sizeof(jsonBuf)) return;
  memcpy(jsonBuf, payload, length);
  jsonBuf[length] = '\0';

  Serial.printf("[MQTT RX] %s: %s\n", topic, jsonBuf);
  dbgPrintf("[MQTT RX] %s: %s\n", topic, jsonBuf);

  JsonDocument doc;
  DeserializationError err = deserializeJson(doc, jsonBuf);
  if (err) return;

  // Power
  if (doc.containsKey("power")) {
    int p = doc["power"];
    acPower = (p == 1);
    sendBlueStarRecord("01", acPower ? "1" : "0");
  }

  // Target Temperature
  if (doc.containsKey("targetTemp")) {
    float t = doc["targetTemp"];
    if (t < 16.0) t = 16.0;
    if (t > 30.0) t = 30.0;
    targetTemp = t;
    int val = (int)(t * 10 + 0.5);
    char buf[4];
    snprintf(buf, sizeof(buf), "%03X", val);
    sendBlueStarRecord("02", String(buf));
  }

  // Mode: 1=Cool, 2=Dry, 3=Fan, 4=Auto
  if (doc.containsKey("mode")) {
    int m = doc["mode"];
    int acM = 2;
    if (m == 1) acM = 2;
    else if (m == 2) acM = 3;
    else if (m == 3) acM = 0;
    else if (m == 4) acM = 4;
    acMode = acM;
    sendBlueStarRecord("03", String(acM));
  }

  // Fan: 1=Quiet, 2=Low, 3=Med, 4=High, 5=Turbo, 6=Auto
  if (doc.containsKey("fan")) {
    int f = doc["fan"];
    int acF = 7;
    if (f == 1) acF = 1;
    else if (f == 2) acF = 2;
    else if (f == 3) acF = 3;
    else if (f == 4) acF = 4;
    else if (f == 5) acF = 6;
    else if (f == 6) acF = 7;
    acFan = acF;
    sendBlueStarRecord("04", String(acF));
  }

  // Vertical Vane / Swing
  if (doc.containsKey("vane")) {
    int pos = doc["vane"];
    if (pos >= 0 && pos <= 6) {
      acVane = pos;
      sendBlueStarRecord("05", String(pos));
    }
  }

  // Horizontal Swing (1=On, 0=Off)
  if (doc.containsKey("hSwing")) {
    bool on = (doc["hSwing"] == 1);
    hSwing = on ? 0 : 6;
    sendBlueStarRecord("06", String(hSwing));
  }

  // 5-in-1 Convertible (1=100%, 2=80%, 3=60%, 4=40%)
  if (doc.containsKey("convertible")) {
    int c = doc["convertible"];
    if (c >= 1 && c <= 4) {
      convertible = c;
      sendBlueStarRecord("55", String(c));
    }
  }

  // Eco
  if (doc.containsKey("eco")) {
    ecoMode = (doc["eco"] == 1);
    sendBlueStarRecord("22", ecoMode ? "1" : "0");
  }

  // Turbo
  if (doc.containsKey("turbo")) {
    turboCool = (doc["turbo"] == 1);
    sendBlueStarRecord("07", turboCool ? "3" : "0");
  }

  // Sleep
  if (doc.containsKey("sleep")) {
    comfortSleep = (doc["sleep"] == 1);
    sendBlueStarRecord("11", comfortSleep ? "1" : "0");
  }

  // Display Light
  if (doc.containsKey("light")) {
    displayLight = (doc["light"] == 1);
    sendBlueStarRecord("15", displayLight ? "1" : "0");
  }

  // Buzzer Mute
  if (doc.containsKey("mute")) {
    buzzerMute = (doc["mute"] == 1);
    sendBlueStarRecord("58", buzzerMute ? "1" : "0");
  }

  publishState();
}

// ==================== 6. NON-BLOCKING MQTT CONNECT ====================
void checkMqtt() {
  if (mqttClient.connected()) return;
  
  uint32_t now = millis();
  if (now - lastMqttReconnectTime > 5000) {
    lastMqttReconnectTime = now;
    dbgPrint("[MQTT] Connecting to Adafruit IO... ");
    String clientId = "BlueStarAC-" + String(random(0xffff), HEX);
    
    if (mqttClient.connect(clientId.c_str(), mqtt_user, mqtt_password)) {
      dbgPrintln("Connected!");
      mqttClient.subscribe(TOPIC_SET);
      sendHandshake();
      publishState();
    } else {
      dbgPrintf("Failed (rc=%d), will retry in background...\n", mqttClient.state());
    }
  }
}

// Process Telnet Live Console
void processTelnet() {
  if (telnetServer.hasClient()) {
    if (!telnetClient || !telnetClient.connected()) {
      if (telnetClient) telnetClient.stop();
      telnetClient = telnetServer.available();
      telnetClient.println("\n=== Blue Star AC MQTT Console (Port 23) ===");
      telnetClient.printf("WiFi: Connected (RSSI: %d dBm) | MQTT: %s (State: %d)\n",
                          WiFi.RSSI(),
                          mqttClient.connected() ? "CONNECTED" : "DISCONNECTED",
                          mqttClient.state());
      telnetClient.println("Commands: [h]andshake, [s]end heartbeat, [q]uery extended diag, [i]nfo, [r]eboot ESP");
    } else {
      WiFiClient rejectClient = telnetServer.available();
      rejectClient.stop();
    }
  }

  while (telnetClient && telnetClient.available()) {
    char c = telnetClient.read();
    if (c == 'r' || c == 'R') {
      telnetClient.println("\n[CMD] Rebooting ESP32...");
      ESP.restart();
    } else if (c == 'h' || c == 'H') {
      telnetClient.println("\n[CMD] Re-running Handshake...");
      sendHandshake();
    } else if (c == 's' || c == 'S') {
      telnetClient.println("\n[CMD] Sending Heartbeat...");
      queueTuyaFrame(CMD_HEARTBEAT);
    } else if (c == 'q' || c == 'Q') {
      telnetClient.println("\n[CMD] Querying Extended Diagnostics (24, 62)...");
      sendBlueStarRecord("24", "0");
      sendBlueStarRecord("62", "0");
    } else if (c == 'i' || c == 'I') {
      telnetClient.printf("\n[INFO] WiFi RSSI: %d dBm | IP: %s\n", WiFi.RSSI(), WiFi.localIP().toString().c_str());
      telnetClient.printf("[INFO] MQTT: %s (rc=%d) | Broker: %s:%d\n", mqttClient.connected() ? "CONNECTED" : "DISCONNECTED", mqttClient.state(), mqtt_server, mqtt_port);
      telnetClient.printf("[INFO] AC Power: %s | Mode: %d | Fan: %d | Target: %.1f C | Room: %.1f C\n", acPower ? "ON" : "OFF", acMode, acFan, targetTemp, roomTemp);
      telnetClient.printf("[INFO] Comp: %ld Hz | Coil: %.1f C | AC Hours: %.1f | Comp Hours: %.1f\n", compressorHz, coilTemp, acRunHours, compRunHours);
    }
  }
}

// ==================== 7. SETUP & LOOP ====================
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n--- Blue Star Smart AC (HiveMQ / Adafruit IO Edition) ---");

  // Set GPIO 17 drive capability to 40mA (GPIO_DRIVE_CAP_3) for strong signaling
  gpio_set_drive_capability((gpio_num_t)AC_TX_PIN, GPIO_DRIVE_CAP_3);

  acSerial.begin(9600, SERIAL_8N1, AC_RX_PIN, AC_TX_PIN);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  Serial.print("[WiFi] Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected! IP: " + WiFi.localIP().toString());

  // Setup Telnet Server
  telnetServer.begin();
  telnetServer.setNoDelay(true);

  // Setup TLS: setInsecure skips root cert checking for light RAM footprint
  espClient.setInsecure();
  mqttClient.setServer(mqtt_server, mqtt_port);
  mqttClient.setCallback(onMqttMessage);
  mqttClient.setBufferSize(512);

  // OTA Setup for Wireless Updates
  ArduinoOTA.setHostname("bluestar-ac");
  ArduinoOTA.begin();

  sendHandshake();
}

void loop() {
  ArduinoOTA.handle();

  checkMqtt();
  if (mqttClient.connected()) {
    mqttClient.loop();
  }

  processIncomingSerial();
  processTxQueue();
  processTelnet();

  // Heartbeat every 15 seconds
  if (millis() - lastHeartbeatTime >= 15000) {
    lastHeartbeatTime = millis();
    if (millis() - lastValidFrameTime > SILENCE_REHANDSHAKE_MS) {
      sendHandshake();
    } else {
      queueTuyaFrame(CMD_HEARTBEAT);
    }
  }
}
