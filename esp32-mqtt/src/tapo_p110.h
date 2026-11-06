#pragma once

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <vector>
#include <string>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <mbedtls/sha1.h>
#include <mbedtls/sha256.h>
#include <mbedtls/aes.h>

/**
 * Tapo P110 KLAP (Key Exchange and Local Authentication Protocol) Client for ESP32
 * Implements hardware-accelerated AES-128-CBC and SHA-256 for local energy monitoring.
 */

struct TapoEnergyData {
  float powerWatts       = 0.0f; // Current active power in Watts
  float todayKwh         = 0.0f; // Cumulative energy consumed today in kWh
  float monthKwh         = 0.0f; // Cumulative energy consumed this month in kWh
  int   todayRuntimeMin  = 0;    // Runtime today in minutes
  int   monthRuntimeMin  = 0;    // Runtime this month in minutes
  bool  relayOn          = false;// Relay state (true = on, false = off)
  bool  online           = false;// Connection status to Tapo P110
  uint32_t lastUpdateMs  = 0;    // Millis timestamp of last successful read
};

class TapoCipher {
public:
  TapoCipher(const std::vector<uint8_t>& localSeed,
             const std::vector<uint8_t>& remoteSeed,
             const std::vector<uint8_t>& authHash) {
    std::vector<uint8_t> localHash = concat(localSeed, remoteSeed, authHash);
    key = keyDerive(localHash);
    auto ivSeqPair = ivDerive(localHash);
    iv = std::get<0>(ivSeqPair);
    seq = std::get<1>(ivSeqPair);
    sig = sigDerive(localHash);
  }

  std::pair<std::vector<uint8_t>, uint32_t> encrypt(const std::string& data) {
    seq += 1;
    std::vector<uint8_t> ivSeqData = ivSeq(seq);

    mbedtls_aes_context aesCtx;
    mbedtls_aes_init(&aesCtx);
    mbedtls_aes_setkey_enc(&aesCtx, key.data(), key.size() * 8);

    std::vector<uint8_t> paddedData = pad(data);
    std::vector<uint8_t> encryptedData(paddedData.size());
    mbedtls_aes_crypt_cbc(&aesCtx, MBEDTLS_AES_ENCRYPT, paddedData.size(),
                          ivSeqData.data(), paddedData.data(), encryptedData.data());
    mbedtls_aes_free(&aesCtx);

    std::vector<uint8_t> seqBytes = toBytes(seq);
    std::vector<uint8_t> combinedData = concat(sig, seqBytes, encryptedData);
    std::vector<uint8_t> signature = sha256(combinedData);

    std::vector<uint8_t> result = concat(signature, encryptedData);
    return { result, seq };
  }

  std::string decrypt(uint32_t seqNum, const std::vector<uint8_t>& cipherData) {
    if (cipherData.size() < 32) return "";

    std::vector<uint8_t> encryptedData(cipherData.begin() + 32, cipherData.end());
    if (encryptedData.empty() || (encryptedData.size() % 16) != 0) return "";

    std::vector<uint8_t> ivSeqData = ivSeq(seqNum);

    mbedtls_aes_context aesCtx;
    mbedtls_aes_init(&aesCtx);
    mbedtls_aes_setkey_dec(&aesCtx, key.data(), key.size() * 8);

    std::vector<uint8_t> decryptedData(encryptedData.size());
    int rc = mbedtls_aes_crypt_cbc(&aesCtx, MBEDTLS_AES_DECRYPT, encryptedData.size(),
                                   ivSeqData.data(), encryptedData.data(), decryptedData.data());
    mbedtls_aes_free(&aesCtx);

    if (rc != 0) return "";
    return unpad(decryptedData);
  }

  static std::vector<uint8_t> sha1(const std::vector<uint8_t>& data) {
    std::vector<uint8_t> hash(20);
    mbedtls_sha1(data.data(), data.size(), hash.data());
    return hash;
  }

  static std::vector<uint8_t> sha256(const std::vector<uint8_t>& data) {
    std::vector<uint8_t> hash(32);
    mbedtls_sha256(data.data(), data.size(), hash.data(), 0);
    return hash;
  }

  static std::string toHexString(const std::vector<uint8_t>& data) {
    std::ostringstream oss;
    for (uint8_t b : data) {
      oss << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(b);
    }
    return oss.str();
  }

  static std::vector<uint8_t> concat(const std::vector<uint8_t>& a, const std::vector<uint8_t>& b) {
    std::vector<uint8_t> c(a);
    c.insert(c.end(), b.begin(), b.end());
    return c;
  }

  static std::vector<uint8_t> concat(const std::vector<uint8_t>& a,
                                     const std::vector<uint8_t>& b,
                                     const std::vector<uint8_t>& c) {
    std::vector<uint8_t> res(a);
    res.insert(res.end(), b.begin(), b.end());
    res.insert(res.end(), c.begin(), c.end());
    return res;
  }

private:
  std::vector<uint8_t> key;
  std::vector<uint8_t> iv;
  uint32_t seq;
  std::vector<uint8_t> sig;

  std::vector<uint8_t> keyDerive(const std::vector<uint8_t>& localHash) {
    std::vector<uint8_t> input = concat({ 'l', 's', 'k' }, localHash);
    auto h = sha256(input);
    return { h.begin(), h.begin() + 16 };
  }

  std::pair<std::vector<uint8_t>, uint32_t> ivDerive(const std::vector<uint8_t>& localHash) {
    std::vector<uint8_t> input = concat({ 'i', 'v' }, localHash);
    auto h = sha256(input);
    std::vector<uint8_t> ivBuf(h.begin(), h.begin() + 12);
    uint32_t s = (static_cast<uint32_t>(h[28]) << 24) |
                 (static_cast<uint32_t>(h[29]) << 16) |
                 (static_cast<uint32_t>(h[30]) << 8)  |
                 (static_cast<uint32_t>(h[31]));
    return { ivBuf, s };
  }

  std::vector<uint8_t> sigDerive(const std::vector<uint8_t>& localHash) {
    std::vector<uint8_t> input = concat({ 'l', 'd', 'k' }, localHash);
    auto h = sha256(input);
    return { h.begin(), h.begin() + 28 };
  }

  std::vector<uint8_t> ivSeq(uint32_t s) {
    std::vector<uint8_t> seqBytes = toBytes(s);
    return concat(iv, seqBytes);
  }

  std::vector<uint8_t> pad(const std::string& data) {
    size_t padLen = 16 - (data.size() % 16);
    std::vector<uint8_t> padded(data.begin(), data.end());
    padded.insert(padded.end(), padLen, static_cast<uint8_t>(padLen));
    return padded;
  }

  std::string unpad(const std::vector<uint8_t>& data) {
    if (data.empty()) return "";
    uint8_t padLen = data.back();
    if (padLen == 0 || padLen > 16 || padLen > data.size()) return "";
    for (size_t i = data.size() - padLen; i < data.size(); i++) {
      if (data[i] != padLen) return "";
    }
    return std::string(data.begin(), data.end() - padLen);
  }

  std::vector<uint8_t> toBytes(uint32_t val) {
    return { static_cast<uint8_t>(val >> 24),
             static_cast<uint8_t>(val >> 16),
             static_cast<uint8_t>(val >> 8),
             static_cast<uint8_t>(val) };
  }
};

class TapoProtocol {
public:
  bool handshake(const String& ipAddress, const String& user, const String& pass) {
    this->ipAddress = ipAddress;
    this->baseUrl   = "http://" + ipAddress;
    this->url       = baseUrl + "/app";
    this->username  = user;
    this->password  = pass;

    if (cipher) {
      delete cipher;
      cipher = nullptr;
    }

    std::vector<uint8_t> userHash = TapoCipher::sha1(toBytes(username));
    std::vector<uint8_t> passHash = TapoCipher::sha1(toBytes(password));
    std::vector<uint8_t> authHash = TapoCipher::sha256(TapoCipher::concat(userHash, passHash));

    std::vector<uint8_t> localSeed = randomBytes(16);
    std::vector<uint8_t> remoteSeed = handshake1(localSeed, authHash);
    if (remoteSeed.empty()) {
      return false;
    }

    if (!handshake2(localSeed, remoteSeed, authHash)) {
      return false;
    }

    cipher = new TapoCipher(localSeed, remoteSeed, authHash);
    return true;
  }

  void rehandshake() {
    if (cipher) {
      delete cipher;
      cipher = nullptr;
    }
    cookie = "";
    delay(150);
    (void)handshake(ipAddress, username, password);
  }

  String sendMessage(const String& message) {
    if (!cipher) return "";

    auto encPair = cipher->encrypt(std::string(message.c_str()));
    auto& encMessage = encPair.first;
    auto& seq = encPair.second;

    std::vector<uint8_t> response;
    int respCode = post("/request?seq=" + String(seq), encMessage, [&response](HTTPClient& http) {
      int sz = http.getSize();
      if (sz <= 0) {
        String body = http.getString();
        response.assign(body.begin(), body.end());
        return;
      }
      response.resize(static_cast<size_t>(sz));
      http.getStream().readBytes(reinterpret_cast<char*>(response.data()), response.size());
    });

    if (respCode != 200 || response.empty()) {
      Serial.printf("[TAPO HTTP] Request failed, code=%d, size=%d\n", respCode, (int)response.size());
      return "";
    }

    std::string dec = cipher->decrypt(seq, response);
    if (dec.empty()) {
      Serial.printf("[TAPO CRYPTO] Decrypt failed, seq=%u, encLen=%d\n", seq, (int)response.size());
      return "";
    }
    return String(dec.c_str());
  }

  bool isReady() const { return cipher != nullptr; }

  ~TapoProtocol() {
    if (cipher) {
      delete cipher;
      cipher = nullptr;
    }
  }

private:
  TapoCipher* cipher = nullptr;
  String cookie      = "";
  String ipAddress   = "";
  String baseUrl     = "";
  String url         = "";
  String username    = "";
  String password    = "";

  static std::vector<uint8_t> toBytes(const String& val) {
    return std::vector<uint8_t>(val.begin(), val.end());
  }

  static String toString(const std::vector<uint8_t>& val) {
    return String(reinterpret_cast<const char*>(val.data()), val.size());
  }

  static std::vector<uint8_t> randomBytes(size_t sz) {
    std::vector<uint8_t> d(sz);
    std::generate(d.begin(), d.end(), [&]() { return random(256); });
    return d;
  }

  int post(const String& endpoint,
           const std::vector<uint8_t>& payload,
           std::function<void(HTTPClient&)> responseHandler,
           bool collectHeaders = false) {
    if (WiFi.status() != WL_CONNECTED) return -1;

    HTTPClient http;
    http.begin(url + endpoint);
    http.addHeader("Connection", "close");

    if (collectHeaders) {
      const char* hKeys[] = { "Set-Cookie" };
      http.collectHeaders(hKeys, 1);
    }

    if (cookie.length() > 0) {
      http.addHeader("Cookie", "TP_SESSIONID=" + cookie);
    }

    http.setTimeout(4000); // 4s timeout prevents blocking
    int respCode = http.POST(const_cast<uint8_t*>(payload.data()), payload.size());
    if (respCode != 200) {
      http.end();
      delay(60);
      return respCode;
    }

    if (collectHeaders) {
      String cStr = http.header("Set-Cookie");
      int sIdx = cStr.indexOf("TP_SESSIONID=");
      if (sIdx >= 0) {
        sIdx += 13;
        int eIdx = cStr.indexOf(";", sIdx);
        cookie = (eIdx > sIdx) ? cStr.substring(sIdx, eIdx) : "";
      } else {
        cookie = "";
      }
    }

    responseHandler(http);
    http.end();
    delay(60);
    return respCode;
  }

  std::vector<uint8_t> handshake1(const std::vector<uint8_t>& localSeed,
                                  const std::vector<uint8_t>& authHash) {
    String respStr;
    int code = post("/handshake1", localSeed, [&respStr](HTTPClient& http) {
      respStr = http.getString();
    }, true);

    Serial.printf("[TAPO DEBUG] Handshake1 HTTP code: %d, bodyLen: %d\n", code, (int)respStr.length());

    if (code != 200 || respStr.length() < 48) {
      Serial.printf("[TAPO DEBUG] Handshake1 failed: HTTP=%d, len=%d\n", code, (int)respStr.length());
      return {};
    }

    std::vector<uint8_t> remoteSeed(respStr.begin(), respStr.begin() + 16);
    std::vector<uint8_t> serverHash(respStr.begin() + 16, respStr.end());
    std::vector<uint8_t> localHash = TapoCipher::sha256(TapoCipher::concat(localSeed, remoteSeed, authHash));
    if (localHash != serverHash) {
      Serial.println("[TAPO DEBUG] Hash mismatch! Check username/password or KLAP version.");
      return {};
    }

    return remoteSeed;
  }

  bool handshake2(const std::vector<uint8_t>& localSeed,
                  const std::vector<uint8_t>& remoteSeed,
                  const std::vector<uint8_t>& authHash) {
    std::vector<uint8_t> payload = TapoCipher::sha256(TapoCipher::concat(remoteSeed, localSeed, authHash));
    String respStr;
    int code = post("/handshake2", payload, [&respStr](HTTPClient& http) {
      respStr = http.getString();
    });
    Serial.printf("[TAPO DEBUG] Handshake2 HTTP code: %d\n", code);
    return (code == 200);
  }
};

class TapoP110 {
public:
  static constexpr const char* TERMINAL_UUID = "00-00-00-00-00-00";

  bool begin(const String& ip, const String& user, const String& pass) {
    this->ip = ip;
    this->user = user;
    this->pass = pass;
    connected = protocol.handshake(ip, user, pass);
    return connected;
  }

  bool isConnected() const { return connected; }

  // Query real-time electrical energy usage from Tapo P110
  bool updateEnergy(TapoEnergyData& out) {
    if (!connected && !begin(ip, user, pass)) {
      out.online = false;
      return false;
    }

    String req = addMeta("{\"method\":\"get_energy_usage\",\"params\":{}}");
    String resp = protocol.sendMessage(req);

    if (resp.length() == 0) {
      protocol.rehandshake();
      resp = protocol.sendMessage(req);
      if (resp.length() == 0) {
        connected = false;
        out.online = false;
        return false;
      }
    }

    JsonDocument doc;
    DeserializationError err = deserializeJson(doc, resp);
    if (err) {
      return false;
    }

    JsonObject res = doc["result"].is<JsonObject>() ? doc["result"] : doc["get_energy_usage"];
    if (res.isNull()) {
      return false;
    }

    // current_power is returned in mW (e.g. 845000 = 845W) or W
    long rawPower = res["current_power"] | 0;
    out.powerWatts = (rawPower > 10000) ? (rawPower / 1000.0f) : static_cast<float>(rawPower);

    long todayWh = res["today_energy"] | 0;
    out.todayKwh = todayWh / 1000.0f;

    long monthWh = res["month_energy"] | 0;
    out.monthKwh = monthWh / 1000.0f;

    out.todayRuntimeMin = res["today_runtime"] | 0;
    out.monthRuntimeMin = res["month_runtime"] | 0;

    out.online = true;
    out.lastUpdateMs = millis();
    connected = true;

    // Check device relay state if present in energy payload
    if (!res["device_on"].isNull()) {
      out.relayOn = res["device_on"].as<bool>();
    } else if (out.powerWatts > 0.5f || out.todayRuntimeMin > 0) {
      out.relayOn = true;
    }

    return true;
  }

  // Fetch device info (specifically relay state and nickname)
  bool updateDeviceInfo(TapoEnergyData& out) {
    if (!connected && !begin(ip, user, pass)) {
      out.online = false;
      return false;
    }

    String req = addMeta("{\"method\":\"get_device_info\",\"params\":{}}");
    String resp = protocol.sendMessage(req);
    if (resp.length() == 0) return false;

    JsonDocument doc;
    if (deserializeJson(doc, resp)) return false;

    JsonObject res = doc["result"].is<JsonObject>() ? doc["result"] : doc["get_device_info"];
    if (!res.isNull() && !res["device_on"].isNull()) {
      out.relayOn = res["device_on"].as<bool>();
      out.online = true;
      return true;
    }
    return false;
  }

  // Switch relay on or off
  bool setRelay(bool on) {
    if (!connected && !begin(ip, user, pass)) return false;

    String params = "{\"device_on\":" + String(on ? "true" : "false") + "}";
    String cmd = addMeta("{\"method\":\"set_device_info\",\"params\":" + params + "}");

    String resp = protocol.sendMessage(cmd);
    if (resp.length() == 0) {
      protocol.rehandshake();
      resp = protocol.sendMessage(cmd);
    }
    return (resp.length() > 0 && resp.indexOf("\"error_code\":0") != -1);
  }

private:
  TapoProtocol protocol;
  String ip;
  String user;
  String pass;
  bool connected = false;

  static uint64_t requestTimeMillis() {
    time_t sec = time(nullptr);
    if (sec <= 100000) return (uint64_t)millis();
    return (uint64_t)sec * 1000ULL + (uint64_t)(millis() % 1000);
  }

  static String addMeta(String json) {
    json.trim();
    int end = json.lastIndexOf('}');
    if (end < 0) return json;
    json.remove(end);
    json += ",\"requestTimeMilis\":" + String((uint64_t)requestTimeMillis());
    json += ",\"terminalUUID\":\"" + String(TERMINAL_UUID) + "\"}";
    return json;
  }
};
