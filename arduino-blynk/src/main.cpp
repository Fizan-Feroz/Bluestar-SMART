/**********************************************************************************
 * Blue Star AC (IC318QNU & similar Smart-Ready models) -> ESP32 DevKit V1 -> Blynk IoT
 * 
 * Hardware:
 *   ESP32 DevKit V1
 *   Blue Star AC Display Board 4-pin Wi-Fi port (Megmeet MD50BS or equivalent)
 * 
 * Pinout:
 *   AC 5V      -> ESP32 VIN (5V)
 *   AC GND     -> ESP32 GND
 *   AC R_WIFI  -> 5k ohm (or 2x 10k in parallel) -> ESP32 GPIO 16 (RX2)
 *                 10k ohm resistor from GPIO 16 to GND (Voltage Divider: 5V -> ~3.3V)
 *   AC T_WIFI  -> ESP32 GPIO 17 (TX2) direct
 * 
 * Features:
 *   - Wireless Over-The-Air (ArduinoOTA) flashing
 *   - Telnet Live Diagnostic Console on port 23
 *   - Real-time raw UART byte inspector
 *   - Blynk 2.0 Cloud & App control
 **********************************************************************************/

#include <Arduino.h>
#include <driver/gpio.h>
#include "soc/gpio_reg.h"

#define BLYNK_PRINT Serial

// ====== 1. Blynk Template Credentials ======
#define BLYNK_TEMPLATE_ID   "TMPL3LTUF8fu5"
#define BLYNK_TEMPLATE_NAME "Blue Star AC"
#define BLYNK_AUTH_TOKEN    "tAtwxap4DmpIjAhdRvXul02cPLXwwRGm"

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include <ArduinoOTA.h>
#include <vector>
#include <deque>

// ====== 2. Wi-Fi Credentials ======
char ssid[] = "Bsnl fiber net 2.4";
char pass[] = "waves123";

// ====== 3. UART Pin Configuration ======
#define AC_RX_PIN 16  // Connects to AC R_WIFI (via voltage divider)
#define AC_TX_PIN 17  // Connects to AC T_WIFI
HardwareSerial acSerial(2); // Hardware UART2

// ====== 4. Telnet Live Debug Server ======
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

// ====== 5. Tuya Protocol Constants ======
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

// Internal state tracking
bool acPower = false;
float targetTemp = 24.0;
int acMode = 2; // 2 = Cool
int acFan = 7;  // 7 = Auto
int acVane = 6; // 6 = Off, 0 = Swing
bool displayLight = true;
float roomTemp = 0.0;
long compressorHz = 0;
float coilTemp = 0.0;

uint32_t lastTxTime = 0;
uint32_t lastRxByteTime = 0;
uint32_t lastValidFrameTime = 0;
uint32_t totalRxBytes = 0;
uint32_t totalTxFrames = 0;

uint32_t lastGpioReg = 0;
uint32_t pinTransitions[32] = {0};

void trackPinTransitions() {
  uint32_t curr = REG_READ(GPIO_IN_REG);
  uint32_t diff = curr ^ lastGpioReg;
  if (diff) {
    for (int p = 0; p < 32; p++) {
      if ((diff >> p) & 1) pinTransitions[p]++;
    }
    lastGpioReg = curr;
  }
}

std::vector<uint8_t> rxBuffer;
std::deque<std::vector<uint8_t>> txQueue;

BlynkTimer timer;

// ====== 6. CRC-16 / MODBUS (Poly 0xA001, Init 0xFFFF) ======
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

// Forward declarations
void sendBlueStarRecord(const String &key, const String &value);
void sendHandshake();

// Queue a raw Tuya frame (55 AA 00 cmd lenH lenL payload sum)
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

// Send a Blue Star DP101 record: *LLKKV...CCCC#
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
  
  dbgPrintf("[AC TX] Queued Record: %s\n", fullRecord.c_str());
  queueTuyaFrame(CMD_DP_SET, payload);
}

// Perform the required Blue Star Tuya Handshake sequence
void sendHandshake() {
  dbgPrintln("[AC] >>> Sending Tuya Handshake sequence to AC...");
  queueTuyaFrame(CMD_PRODUCT_QUERY);
  queueTuyaFrame(CMD_WORKING_MODE);
  queueTuyaFrame(CMD_NET_STATUS, {NET_STATUS_CLOUD});
  queueTuyaFrame(CMD_QUERY_ALL);
  queueTuyaFrame(CMD_HEARTBEAT);
  sendBlueStarRecord("00", "0"); // Query full state dump
}

// Process Blue Star key-value records
void handleBlueStarKey(const String &key, const String &value) {
  dbgPrintf("[AC RX DECODED] Key: %s | Value: %s\n", key.c_str(), value.c_str());
  
  if (key == "01") { // Power
    acPower = (value == "1");
    Blynk.virtualWrite(V0, acPower ? 1 : 0);
  }
  else if (key == "02") { // Setpoint in °C x 10 (hex)
    long raw = strtol(value.c_str(), nullptr, 16);
    targetTemp = raw / 10.0f;
    Blynk.virtualWrite(V1, targetTemp);
  }
  else if (key == "03") { // Mode (0 fan, 2 cool, 3 dry, 4 auto)
    int m = value.toInt();
    acMode = m;
    int blynkMode = 1;
    if (m == 2) blynkMode = 1;      // Cool
    else if (m == 3) blynkMode = 2; // Dry
    else if (m == 0) blynkMode = 3; // Fan
    else if (m == 4) blynkMode = 4; // Auto
    Blynk.virtualWrite(V2, blynkMode);
  }
  else if (key == "04") { // Fan (1 quiet, 2 low, 3 med, 4 high, 6 turbo, 7 auto)
    int f = value.toInt();
    acFan = f;
    int blynkFan = 6;
    if (f == 1) blynkFan = 1;      // Quiet
    else if (f == 2) blynkFan = 2; // Low
    else if (f == 3) blynkFan = 3; // Med
    else if (f == 4) blynkFan = 4; // High
    else if (f == 6) blynkFan = 5; // Turbo
    else if (f == 7) blynkFan = 6; // Auto
    Blynk.virtualWrite(V3, blynkFan);
  }
  else if (key == "05") { // Vertical Vane (0: Swing, 1: Top ... 5: Bottom, 6: Off)
    acVane = value.toInt();
    Blynk.virtualWrite(V6, acVane);
  }
  else if (key == "06") { // Horizontal Swing (4-way)
    int hSwing = value.toInt();
    Blynk.virtualWrite(V7, (hSwing == 0) ? 1 : 0);
  }
  else if (key == "55") { // Convertible Capacity (1=100%, 2=80%, 3=60%, 4=40%)
    int conv = value.toInt();
    Blynk.virtualWrite(V8, conv);
  }
  else if (key == "15") { // Display Light
    displayLight = (value == "1");
    Blynk.virtualWrite(V4, displayLight ? 1 : 0);
  }
  else if (key == "22") { // Eco Mode / Energy Save ("E" on display)
    bool eco = (value == "1");
    Blynk.virtualWrite(V9, eco ? 1 : 0);
  }
  else if (key == "07") { // 5-in-1 Turbo Cool ("HC" on display)
    bool turbo = (value == "3");
    Blynk.virtualWrite(V10, turbo ? 1 : 0);
  }
  else if (key == "11") { // Comfort Sleep
    bool sleep = (value == "1");
    Blynk.virtualWrite(V11, sleep ? 1 : 0);
  }
  else if (key == "58") { // Buzzer Mute
    bool muted = (value == "1");
    Blynk.virtualWrite(V15, muted ? 1 : 0);
  }
  else if (key == "24") { // Compressor Inverter Speed
    if (value.length() >= 2) {
      long hz = strtol(value.substring(0, 2).c_str(), nullptr, 16);
      if (!acPower) hz = 0;
      compressorHz = hz;
      Blynk.virtualWrite(V17, compressorHz);
      dbgPrintf("\n[DIAG] Key 24 -> Compressor Speed: %ld Hz (Blynk V17)\n", compressorHz);
    }
  }
  else if (key == "25") {
    dbgPrintf("[DIAG] Key 25 (Outdoor Sub-telemetry): Raw = %s\n", value.c_str());
  }
  else if (key == "62") { // Internal coil/exchanger temp
    long raw = strtol(value.c_str(), nullptr, 16);
    coilTemp = raw / 10.0f;
    Blynk.virtualWrite(V18, coilTemp);
    dbgPrintf("\n[DIAG] Key 62 -> Coil Temp: %.1f C (Blynk V18)\n", coilTemp);
  }
  else if (key == "29") {
    dbgPrintf("[DIAG] Key 29 (Operating Profile Dump): %s\n", value.c_str());
  }
  else if (key == "61") {
    dbgPrintf("[DIAG] Key 61 (Mainboard Hardware ID): %s\n", value.c_str());
  }
  else if (key == "59") {
    dbgPrintf("[DIAG] Key 59 (High-Res Compressor Counter): %s\n", value.c_str());
  }
  else if (key == "60") {
    dbgPrintf("[DIAG] Key 60 (Secondary Offset Counter): %s\n", value.c_str());
  }
  else if (key == "13") {
    int s = value.toInt();
    const char *season = (s == 1) ? "Autumn" : (s == 2) ? "Summer" : (s == 3) ? "Monsoon" : "Off";
    dbgPrintf("[DIAG] Key 13 (Climate Season Mode): %s (%d)\n", season, s);
  }
  else if (key == "08") {
    dbgPrintf("[DIAG] Key 08 (Timer Active Flags): %s\n", value.c_str());
  }
  else if (key == "09") {
    long mins = strtol(value.c_str(), nullptr, 16);
    dbgPrintf("[DIAG] Key 09 (On-Timer Countdown): %ld minutes\n", mins);
  }
  else if (key == "10") {
    long mins = strtol(value.c_str(), nullptr, 16);
    dbgPrintf("[DIAG] Key 10 (Off-Timer Countdown): %ld minutes\n", mins);
  }
  else if (key == "44") { // Total AC On-time (Lifetime Hours)
    long raw = strtol(value.c_str(), nullptr, 16);
    float hours = raw / 4.0f;
    Blynk.virtualWrite(V13, hours);
  }
  else if (key == "43") { // Compressor Run-time (Lifetime Hours)
    long raw = strtol(value.c_str(), nullptr, 16);
    float hours = raw / 4.0f;
    Blynk.virtualWrite(V14, hours);
  }
  else if (key == "99") { // Room Temperature in °C x 10 (hex)
    long raw = strtol(value.c_str(), nullptr, 16);
    roomTemp = raw / 10.0f;
    Blynk.virtualWrite(V5, roomTemp);
    dbgPrintf("[AC] Room Temperature: %.1f °C\n", roomTemp);
  }
  else if (key == "00") { // Full State Dump
    if (value.length() >= 34) {
      acPower = (value.charAt(0) == '1');
      Blynk.virtualWrite(V0, acPower ? 1 : 0);
      
      String tHex = value.substring(1, 4);
      targetTemp = strtol(tHex.c_str(), nullptr, 16) / 10.0f;
      Blynk.virtualWrite(V1, targetTemp);
      
      acMode = value.substring(4, 5).toInt();
      int bMode = (acMode == 2) ? 1 : (acMode == 3) ? 2 : (acMode == 0) ? 3 : 4;
      Blynk.virtualWrite(V2, bMode);
      
      acFan = value.substring(5, 6).toInt();
      int bFan = (acFan == 1) ? 1 : (acFan == 2) ? 2 : (acFan == 3) ? 3 : (acFan == 4) ? 4 : (acFan == 6) ? 5 : 6;
      Blynk.virtualWrite(V3, bFan);
      
      acVane = value.substring(6, 7).toInt();
      Blynk.virtualWrite(V6, acVane);

      int hSwing = value.substring(7, 8).toInt();
      Blynk.virtualWrite(V7, (hSwing == 0) ? 1 : 0);
      
      displayLight = (value.charAt(23) == '1');
      Blynk.virtualWrite(V4, displayLight ? 1 : 0);
      
      String rHex = value.substring(31, 34);
      roomTemp = strtol(rHex.c_str(), nullptr, 16) / 10.0f;
      Blynk.virtualWrite(V5, roomTemp);

      if (value.length() >= 51) {
        float compHours = strtol(value.substring(39, 43).c_str(), nullptr, 16) / 4.0f;
        float acHours = strtol(value.substring(43, 51).c_str(), nullptr, 16) / 4.0f;
        Blynk.virtualWrite(V13, acHours);
        Blynk.virtualWrite(V14, compHours);
      }
      if (value.length() > 103) {
        bool filterAlert = (value.charAt(103) == '1');
        Blynk.virtualWrite(V16, filterAlert ? 1 : 0);
      }
    }
  }
}

// Parse string records: *LLKKV...CCCC#
void parseBlueStarRecord(const String &rec) {
  if (!rec.startsWith("*") || !rec.endsWith("#") || rec.length() < 9) return;
  
  String body = rec.substring(0, rec.length() - 5);
  String crcExpectedStr = rec.substring(rec.length() - 5, rec.length() - 1);
  uint16_t crcCalc = crc16_modbus(body.c_str(), body.length());
  char crcBuf[5];
  snprintf(crcBuf, sizeof(crcBuf), "%04X", crcCalc);
  if (crcExpectedStr != String(crcBuf)) {
    dbgPrintf("[AC WARN] CRC mismatch! Expected: %s, Calc: %s, Body: %s\n", crcExpectedStr.c_str(), crcBuf, body.c_str());
    return;
  }
  
  String key = body.substring(3, 5);
  String val = body.substring(5);
  handleBlueStarKey(key, val);
}

// Parse DP datapoints inside cmd 0x07 / 0x06
void handleTuyaDatapoints(const uint8_t *data, size_t len) {
  size_t idx = 0;
  while (idx + 4 <= len) {
    uint8_t dpId = data[idx++];
    uint8_t dpType = data[idx++];
    uint16_t dpLen = (data[idx] << 8) | data[idx + 1];
    idx += 2;
    if (idx + dpLen > len) break;
    
    if (dpId == DP_RECORD && dpType == 0x03) { // String DP101
      String rec = "";
      for (size_t i = 0; i < dpLen; i++) rec += (char)data[idx + i];
      parseBlueStarRecord(rec);
    }
    idx += dpLen;
  }
}

// Handle complete incoming Tuya frame
void handleTuyaFrame(uint8_t cmd, const uint8_t *payload, size_t len) {
  lastValidFrameTime = millis();
  dbgPrintf("[AC RX FRAME] Tuya Cmd: 0x%02X | Payload Len: %u\n", cmd, (unsigned int)len);
  
  if (cmd == CMD_DP_REPORT || cmd == CMD_DP_SET) {
    handleTuyaDatapoints(payload, len);
  } else if (cmd == CMD_HEARTBEAT) {
    if (len > 0 && payload[0] == 0x00) {
      dbgPrintln("[AC] MCU reported restart, re-handshaking...");
      sendHandshake();
    } else {
      dbgPrintln("[AC] Heartbeat ACK received from AC.");
    }
  } else if (cmd == CMD_PRODUCT_QUERY) {
    dbgPrintln("[AC] Product Query ACK received.");
  } else if (cmd == CMD_WORKING_MODE) {
    dbgPrintln("[AC] Working Mode ACK received.");
  }
}

// UART byte receiver state machine with RAW BYTE SNIFFER
void processIncomingSerial() {
  while (acSerial.available()) {
    uint8_t b = acSerial.read();
    totalRxBytes++;
    
    // Print raw byte stream
    dbgPrintf("%02X ", b);
    
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
    
    // Checksum verification
    uint8_t sum = 0;
    for (size_t i = 0; i < frameLen - 1; i++) sum += rxBuffer[i];
    dbgPrintln();
    if (sum == rxBuffer[frameLen - 1]) {
      handleTuyaFrame(rxBuffer[3], &rxBuffer[6], payloadLen);
    } else {
      dbgPrintf("[AC WARN] Tuya frame checksum error! Calc: %02X != Expected: %02X\n", sum, rxBuffer[frameLen - 1]);
    }
    rxBuffer.erase(rxBuffer.begin(), rxBuffer.begin() + frameLen);
  }
}

// Check TX queue with mandatory 400ms spacing (rxBuffer check removed so transmission never locks)
void processTxQueue() {
  if (!txQueue.empty() && millis() - lastTxTime >= TX_SPACING_MS) {
    auto &frame = txQueue.front();
    acSerial.write(frame.data(), frame.size());
    acSerial.flush();
    totalTxFrames++;
    lastTxTime = millis();
    
    dbgPrint("[AC RAW TX] ");
    for (uint8_t b : frame) {
      dbgPrintf("%02X ", b);
    }
    dbgPrintln();
    
    txQueue.pop_front();
  }
}

// Handle incoming Telnet diagnostic console commands
void processTelnet() {
  if (telnetServer.hasClient()) {
    if (!telnetClient || !telnetClient.connected()) {
      if (telnetClient) telnetClient.stop();
      telnetClient = telnetServer.available();
      telnetClient.println("\n==================================================");
      telnetClient.println(" Blue Star AC Live Diagnostic Console (ESP32)");
      telnetClient.println(" Model: IC318QNU | Blynk IoT Controller");
      telnetClient.println(" Commands:");
      telnetClient.println("   h -> Trigger Tuya Handshake Sequence");
      telnetClient.println("   p -> Toggle Power (01)");
      telnetClient.println("   d -> Request State Dump (00)");
      telnetClient.println("   + -> Temp Up 1 deg C");
      telnetClient.println("   - -> Temp Down 1 deg C");
      telnetClient.println("   s -> Send Heartbeat");
      telnetClient.println("==================================================");
    } else {
      WiFiClient rejectClient = telnetServer.available();
      rejectClient.stop();
    }
  }

  while (telnetClient && telnetClient.available()) {
    char c = telnetClient.read();
    if (c == 'h' || c == 'H') {
      telnetClient.println("\n[CMD] Manual Handshake triggered!");
      sendHandshake();
    } else if (c == 'p' || c == 'P') {
      acPower = !acPower;
      telnetClient.printf("\n[CMD] Toggling Power -> %d\n", acPower ? 1 : 0);
      sendBlueStarRecord("01", acPower ? "1" : "0");
    } else if (c == 'd' || c == 'D') {
      telnetClient.println("\n[CMD] Requesting full state dump (00)...");
      sendBlueStarRecord("00", "0");
    } else if (c == '+') {
      targetTemp += 1.0;
      if (targetTemp > 30.0) targetTemp = 30.0;
      int val = (int)(targetTemp * 10 + 0.5);
      char buf[4];
      snprintf(buf, sizeof(buf), "%03X", val);
      telnetClient.printf("\n[CMD] Temp Up -> %.1f C\n", targetTemp);
      sendBlueStarRecord("02", String(buf));
    } else if (c == '-') {
      targetTemp -= 1.0;
      if (targetTemp < 16.0) targetTemp = 16.0;
      int val = (int)(targetTemp * 10 + 0.5);
      char buf[4];
      snprintf(buf, sizeof(buf), "%03X", val);
      telnetClient.printf("\n[CMD] Temp Down -> %.1f C\n", targetTemp);
      sendBlueStarRecord("02", String(buf));
    } else if (c == 's' || c == 'S') {
      telnetClient.println("\n[CMD] Sending Heartbeat...");
      queueTuyaFrame(CMD_HEARTBEAT);
    } else if (c == 'q' || c == 'Q') {
      telnetClient.println("\n[CMD] Querying Extended Diagnostics (24, 25, 62, 29, 61, 59, 60, 13)...");
      sendBlueStarRecord("24", "0");
      sendBlueStarRecord("25", "0");
      sendBlueStarRecord("62", "0");
      sendBlueStarRecord("29", "0");
      sendBlueStarRecord("61", "0");
      sendBlueStarRecord("59", "0");
      sendBlueStarRecord("60", "0");
      sendBlueStarRecord("13", "0");
    }
  }
}

// ==================== BLYNK HANDLERS ====================

// V0: AC Power
BLYNK_WRITE(V0) {
  int p = param.asInt();
  acPower = (p == 1);
  if (!acPower) {
    compressorHz = 0;
    Blynk.virtualWrite(V17, 0);
  }
  dbgPrintf("[Blynk] Power command: %d\n", p);
  sendBlueStarRecord("01", acPower ? "1" : "0");
}

// V1: Target Temperature
BLYNK_WRITE(V1) {
  float temp = param.asFloat();
  if (temp < 16.0) temp = 16.0;
  if (temp > 30.0) temp = 30.0;
  targetTemp = temp;
  int val = (int)(temp * 10 + 0.5);
  char buf[4];
  snprintf(buf, sizeof(buf), "%03X", val);
  dbgPrintf("[Blynk] Set Temp: %.1f C (Hex: %s)\n", temp, buf);
  sendBlueStarRecord("02", String(buf));
}

// V2: Operation Mode (1: Cool, 2: Dry, 3: Fan, 4: Auto)
BLYNK_WRITE(V2) {
  int m = param.asInt();
  int acM = 2; // Default Cool
  if (m == 1) acM = 2;      // Cool
  else if (m == 2) acM = 3; // Dry
  else if (m == 3) acM = 0; // Fan
  else if (m == 4) acM = 4; // Auto
  acMode = acM;
  dbgPrintf("[Blynk] Mode: %d -> AC: %d\n", m, acM);
  sendBlueStarRecord("03", String(acM));
}

// V3: Fan Speed (1: Quiet, 2: Low, 3: Med, 4: High, 5: Turbo, 6: Auto)
BLYNK_WRITE(V3) {
  int f = param.asInt();
  int acF = 7; // Default Auto
  if (f == 1) acF = 1;      // Quiet
  else if (f == 2) acF = 2; // Low
  else if (f == 3) acF = 3; // Med
  else if (f == 4) acF = 4; // High
  else if (f == 5) acF = 6; // Turbo
  else if (f == 6) acF = 7; // Auto
  acFan = acF;
  dbgPrintf("[Blynk] Fan Speed: %d -> AC: %d\n", f, acF);
  sendBlueStarRecord("04", String(acF));
}

// V4: Display Light
BLYNK_WRITE(V4) {
  displayLight = (param.asInt() == 1);
  dbgPrintf("[Blynk] Display Light: %d\n", displayLight ? 1 : 0);
  sendBlueStarRecord("15", displayLight ? "1" : "0");
}

// V6: Vertical Louver Vane / Swing (0: Swing, 1: Top ... 5: Bottom, 6: Off)
BLYNK_WRITE(V6) {
  int pos = param.asInt();
  if (pos >= 0 && pos <= 6) {
    acVane = pos;
    dbgPrintf("[Blynk] Vertical Vane: %d\n", pos);
    sendBlueStarRecord("05", String(pos));
  }
}

// V7: Horizontal Louver Swing (4-way) (1: Swing on, 0: Swing off)
BLYNK_WRITE(V7) {
  bool hSwing = (param.asInt() == 1);
  int val = hSwing ? 0 : 6;
  dbgPrintf("[Blynk] Horizontal Swing: %d -> AC: %d\n", hSwing ? 1 : 0, val);
  sendBlueStarRecord("06", String(val));
}

// V8: Convertible Capacity Mode (1: 100%, 2: 80%, 3: 60%, 4: 40%)
BLYNK_WRITE(V8) {
  int cap = param.asInt();
  if (cap >= 1 && cap <= 4) {
    dbgPrintf("[Blynk] Convertible Capacity: %d\n", cap);
    sendBlueStarRecord("55", String(cap));
  }
}

// V9: Eco Mode / Energy Save (1: Eco On, 0: Eco Off) -> Displays "E" on IDU
BLYNK_WRITE(V9) {
  bool eco = (param.asInt() == 1);
  dbgPrintf("[Blynk] Eco Mode: %d\n", eco ? 1 : 0);
  sendBlueStarRecord("22", eco ? "1" : "0");
}

// V10: 5-in-1 Turbo Cool (1: Turbo On, 0: Turbo Off) -> Displays "HC" on IDU
BLYNK_WRITE(V10) {
  bool turbo = (param.asInt() == 1);
  dbgPrintf("[Blynk] Turbo Cool: %d\n", turbo ? 1 : 0);
  sendBlueStarRecord("07", turbo ? "3" : "0");
}

// V11: Comfort Sleep Mode (1: Sleep On, 0: Sleep Off)
BLYNK_WRITE(V11) {
  bool sleep = (param.asInt() == 1);
  dbgPrintf("[Blynk] Sleep Mode: %d\n", sleep ? 1 : 0);
  sendBlueStarRecord("11", sleep ? "1" : "0");
}

// V15: Buzzer Mute (1: Mute On, 0: Mute Off)
BLYNK_WRITE(V15) {
  bool mute = (param.asInt() == 1);
  dbgPrintf("[Blynk] Buzzer Mute: %d\n", mute ? 1 : 0);
  sendBlueStarRecord("58", mute ? "1" : "0");
}

// V19: On-Demand Diagnostics Refresh (Queries Compressor Hz & Coil Temp)
BLYNK_WRITE(V19) {
  if (param.asInt() == 1 && acPower) {
    dbgPrintln("[Blynk] On-demand Diagnostic Refresh requested...");
    sendBlueStarRecord("24", "0");
    sendBlueStarRecord("62", "0");
  }
}

// When Blynk connects, send initial handshake if needed
BLYNK_CONNECTED() {
  dbgPrintln("[Blynk] Connected to Blynk Cloud!");
  sendHandshake();
}

// Heartbeat & Watchdog timer routine (called every 15s - 100% silent)
void periodicHeartbeat() {
  // Silent Tuya heartbeat - MCU answers with 0x00 without beeping
  queueTuyaFrame(CMD_HEARTBEAT);
}

// Diagnostic status beacon (local Wi-Fi only, zero AC serial commands)
void periodicBeacon() {
  dbgPrintf("[BEACON] WiFi: %d dBm | Blynk: %s | Total RX: %u | TX: %u | AC State: %s, %.1f C, Fan:%d, Vane:%d\n",
            WiFi.RSSI(),
            Blynk.connected() ? "ONLINE" : "OFFLINE",
            totalRxBytes,
            totalTxFrames,
            acPower ? "ON" : "OFF",
            targetTemp,
            acFan,
            acVane);
}

// ==================== SETUP & LOOP ====================

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n--- Blue Star AC Controller (ESP32 DevKit V1) ---");
  
  // Set GPIO 17 drive capability to 40mA (GPIO_DRIVE_CAP_3) for strong signaling
  gpio_set_drive_capability((gpio_num_t)AC_TX_PIN, GPIO_DRIVE_CAP_3);

  // Initialize UART2 for Blue Star AC
  acSerial.begin(9600, SERIAL_8N1, AC_RX_PIN, AC_TX_PIN);

  
  // Connect to Wi-Fi and Blynk
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  
  // Start Telnet Live Diagnostic Console on port 23
  telnetServer.begin();
  telnetServer.setNoDelay(true);
  
  // Periodic timers
  timer.setInterval(15000L, periodicHeartbeat);
  timer.setInterval(10000L, periodicBeacon);
  
  // Setup ArduinoOTA for wireless firmware flashing
  ArduinoOTA.setHostname("bluestar-ac");
  ArduinoOTA.onStart([]() {
    String type = (ArduinoOTA.getCommand() == U_FLASH) ? "sketch" : "filesystem";
    dbgPrintln("[OTA] Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {
    dbgPrintln("\n[OTA] Update complete!");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    // Keep progress concise
  });
  ArduinoOTA.onError([](ota_error_t error) {
    dbgPrintf("[OTA] Error[%u]\n", error);
  });
  ArduinoOTA.begin();
  dbgPrintf("[OTA] ArduinoOTA Ready. IP: %s\n", WiFi.localIP().toString().c_str());

  // Initial handshake with AC
  sendHandshake();
}

void loop() {
  trackPinTransitions();
  ArduinoOTA.handle();
  Blynk.run();
  timer.run();
  processIncomingSerial();
  processTxQueue();
  processTelnet();
}
