# Blue Star Smart AC (IC318QNU) — Blynk Setup Guide

This guide walks you through setting up your **ESP32 DevKit V1** with **Blynk IoT** to control your Blue Star AC without Home Assistant, complete with a web dashboard, mobile app, and Siri Shortcuts.

---

## 1. Hardware Connections & Pinout

### Connection Table:

| AC Indoor Display Header | Header Function | Recommended Wire Color | ESP32 DevKit V1 Pin | Connection Details & Circuit |
|---|---|---|---|---|
| **`5V`** | 5V DC Supply | 🔴 **Red** | **`VIN`** (or `5V`) | Direct wire (powers ESP32 from AC) |
| **`GND`** | Ground | ⚫ **Black** | **`GND`** | Direct wire (common ground) |
| **`T_WIFI`** | AC RX (Receive) | 🟢 **Green** | **`GPIO 17 (TX2)`** | **Direct wire** (AC accepts 3.3V logic) |
| **`R_WIFI`** | AC TX (5V Transmit) | 🟡 **Yellow** | **`GPIO 16 (RX2)`** | **Through Voltage Divider (5V → 3.3V):**<br>• $5\text{ k}\Omega$ in series with the line<br>• $10\text{ k}\Omega$ from GPIO 16 to Ground |

> 📌 **Why GPIO 16 & GPIO 17 on ESP32 DevKit V1?**  
> On classic ESP32 DevKit boards, `GPIO 1 (TX0)` and `GPIO 3 (RX0)` are hardwired to the onboard CP2102/CH340 USB-to-Serial chip. Connecting the AC to GPIO 3 will cause electrical bus contention and flashing failures. We use hardware **UART2 (`GPIO 16` as RX and `GPIO 17` as TX)** which leaves the USB port free for programming and debugging.

---

### Circuit & Voltage Divider Diagram

```text
  AC Display Board                                     ESP32 DevKit V1
 (4-Pin Wi-Fi Port)                                     (30/36 Pin DIP)
┌──────────────────┐                                 ┌──────────────────┐
│                  │                                 │                  │
│ [5V] ────────────┼────────── Red Wire ─────────────┼──────────> [VIN] │
│                  │                                 │                  │
│ [GND] ───────────┼──────┬─── Black Wire ───────────┼──────────> [GND] │
│                  │      │                          │                  │
│                  │      │    ┌───────────────┐     │                  │
│                  │      └───┤ 10 kΩ Resistor │     │                  │
│                  │           └───────┬───────┘     │                  │
│                  │                   │ (3.3V tap)  │                  │
│ [R_WIFI] (5V) ───┼─[ 5 kΩ Resistor ]─┴─────────────┼──> [GPIO 16 (RX2)]
│                  │                                 │                  │
│ [T_WIFI] ◄───────┼────────── Green Wire ───────────┼──── [GPIO 17 (TX2)]
│                  │                                 │                  │
└──────────────────┘                                 └──────────────────┘
```

> 💡 **Resistor Tip:**  
> If you don't have a $5\text{ k}\Omega$ resistor, connect **two $10\text{ k}\Omega$ resistors in parallel** (side-by-side) to create $5\text{ k}\Omega$. Then use a third $10\text{ k}\Omega$ resistor to Ground. Total: 3 $\times$ $10\text{ k}\Omega$ resistors.

Full vector diagram: [**`wiring_devkit_v1.svg`**](wiring_devkit_v1.svg)

> ⚠️ **CRITICAL SAFETY WARNINGS:**
> 1. **Never connect USB while powered from AC:** The ESP32 DevKit V1 can be damaged or back-power your PC if both the AC's 5V pin and USB are plugged in simultaneously. Flash firmware on your workbench first via USB, unplug USB, and only then connect to the AC.
> 2. **Switch OFF AC mains breaker** before opening the indoor unit casing. Mains voltage (230V) is present inside the indoor unit!

---

## 2. Blynk Cloud Setup (blynk.cloud)

1. Log in to [blynk.cloud](https://blynk.cloud) (or create a free account).
2. Go to **Developer Zone** $\to$ **Templates** $\to$ **+ New Template**:
   - **Name:** `Blue Star AC`
   - **Hardware:** `ESP32`
   - **Connection Type:** `WiFi`
3. Click on the **Datastreams** tab $\to$ **+ New Datastream** $\to$ **Virtual Pin**:

| Pin | Name | Data Type | Min | Max | Default | Units | Function |
|---|---|---|---|---|---|---|---|
| **`V0`** | Power | Integer | 0 | 1 | 0 | - | AC Power (0=Off, 1=On) |
| **`V1`** | Target Temp | Double | 16.0 | 30.0 | 24.0 | °C | Target Temperature Setpoint |
| **`V2`** | Mode | Integer | 1 | 4 | 1 | - | 1=Cool, 2=Dry, 3=Fan, 4=Auto |
| **`V3`** | Fan Speed | Integer | 1 | 6 | 6 | - | 1=Quiet, 2=Low, 3=Med, 4=High, 5=Turbo, 6=Auto |
| **`V4`** | Display Light | Integer | 0 | 1 | 0 | - | LED Display on Indoor Unit |
| **`V5`** | Room Temp | Double | 0.0 | 50.0 | 0.0 | °C | Live Room Ambient Temperature |
| **`V6`** | Vertical Vane | Integer | 0 | 6 | 0 | - | 0=Auto Swing, 1=Top ... 5=Bottom, 6=Stop |
| **`V7`** | Horizontal Swing| Integer| 0 | 1 | 0 | - | 4-Way Left/Right Motorized Oscillation |
| **`V8`** | 5 in 1 convertible| Integer| 1 | 4 | 1 | - | Capacity: 1=100%, 2=80%, 3=60%, 4=40% |
| **`V9`** | Eco Mode | Integer | 0 | 1 | 0 | - | Energy Save (24°C + Low Fan, "E" on display)|
| **`V10`**| Turbo Cool | Integer | 0 | 1 | 0 | - | Rapid Cooling (16°C, "HC" on display, 20m) |
| **`V11`**| Comfort Sleep | Integer | 0 | 1 | 0 | - | Sleep Mode (+1°C/hr ramp for 2 hours) |
| **`V13`** | AC Run Hours | Double | 0.0 | 99999.0 | 0.0 | hrs | Total Lifetime Mains Power Hours |
| **`V14`** | Comp Run Hours| Double| 0.0 | 99999.0 | 0.0 | hrs | Total Lifetime Compressor Motor Hours |
| **`V15`** | Buzzer Mute | Integer | 0 | 1 | 0 | - | Buzzer Mute (1=Mute, 0=Beep) |
| **`V16`** | Filter Alert | Integer | 0 | 1 | 0 | - | Filter Clean Alert ("FC" on display) |
| **`V17`** | Compressor Speed | Integer | 0 | 80 | 0 | Hz | Inverter Compressor Frequency (Live Motor Speed) |
| **`V18`** | Coil Temp | Double | -10.0 | 60.0 | 0.0 | °C | Indoor Heat Exchanger / Coil Temperature |
| **`V19`** | Diag Refresh | Integer | 0 | 1 | 0 | - | On-Demand Telemetry Trigger (Queries Hz & Coil Temp) |

4. Go to **Web Dashboard** tab:
   - Drag a **Switch** widget $\to$ Assign to `V0` (Power)
   - Drag a **Slider** or **Step** widget $\to$ Assign to `V1` (Target Temp)
   - Drag a **Segmented Switch** $\to$ Assign to `V2` (Mode: 1=Cool, 2=Dry, 3=Fan, 4=Auto)
   - Drag a **Segmented Switch** $\to$ Assign to `V3` (Fan: 1=Quiet, 2=Low, 3=Med, 4=High, 5=Turbo, 6=Auto)
   - Drag a **Switch** widget $\to$ Assign to `V4` (Display Light)
   - Drag a **Value Display** or **Gauge** $\to$ Assign to `V5` (Room Temp)
   - Drag a **Segmented Switch** or **Dropdown** $\to$ Assign to `V6` (Vertical Louver: 0=Auto Swing, 1=Top, 2=Mid-Top, 3=Mid, 4=Mid-Bottom, 5=Bottom, 6=Stop)
   - Drag a **Switch** widget $\to$ Assign to `V7` (Horizontal 4-Way Swing: 1=On, 0=Off)
   - Drag a **Segmented Switch** $\to$ Assign to `V8` (5-in-1 Convertible: 1=100%, 2=80%, 3=60%, 4=40%)
   - Drag a **Switch** widget $\to$ Assign to `V9` (Eco Mode / Energy Save)
   - Drag a **Switch** widget $\to$ Assign to `V10` (5-in-1 Turbo Cool)
   - Drag a **Switch** widget $\to$ Assign to `V11` (Comfort Sleep)
   - Drag a **Value Display** widget $\to$ Assign to `V13` (Total AC Run Hours)
   - Drag a **Value Display** widget $\to$ Assign to `V14` (Compressor Run Hours)
   - Drag a **Switch** widget $\to$ Assign to `V15` (Buzzer Mute)
   - Drag a **LED** widget $\to$ Assign to `V16` (Filter Clean Alert / "FC")
   - Drag a **Gauge** widget $\to$ Assign to `V17` (Compressor Inverter Speed in Hz, Max: 70)
   - Drag a **Value Display** or **Gauge** $\to$ Assign to `V18` (Indoor Cooling Coil Temp in °C)
   - Drag a **Button** widget $\to$ Assign to `V19` (Mode: Push / Momentary, Label: "Refresh Diag")
5. Save the Template.
6. Go to **Devices** $\to$ **+ Add Device** $\to$ **From Template** $\to$ Select `Blue Star AC`.
7. Copy the **Template ID**, **Template Name**, and **Auth Token** shown at the top of the device page.

---

## 3. Flashing the ESP32

1. Open **Arduino IDE**.
2. Go to **Library Manager** (`Ctrl+Shift+I` or `Cmd+Shift+I`) and install:
   - `Blynk` by *Volodymyr Shymanskyy* (version 1.3+).
3. Under **Tools $\to$ Board**, select **ESP32 Dev Module**.
4. Open [bluestar_blynk_esp32.ino](bluestar_blynk_esp32/bluestar_blynk_esp32.ino).
5. Paste your Blynk credentials at lines 28–30:
   ```cpp
   #define BLYNK_TEMPLATE_ID   "TMPLxxxxxx"
   #define BLYNK_TEMPLATE_NAME "Blue Star AC"
   #define BLYNK_AUTH_TOKEN    "Your_Auth_Token_Here"
   ```
6. Enter your Wi-Fi credentials at lines 39–40:
   ```cpp
   char ssid[] = "YOUR_WIFI_SSID";
   char pass[] = "YOUR_WIFI_PASSWORD";
   ```
7. Plug your ESP32 DevKit V1 into your PC via USB and click **Upload**.

---

## 4. Mobile App Setup (Blynk IoT on iOS)

1. Open the **Blynk IoT** app on your iPhone (logged into the same account).
2. Tap your **Blue Star AC** device.
3. Tap the **Wrench/Edit icon** at the top right to design your mobile canvas:
   - Add a **Button / Switch** for Power (`V0`).
   - Add a **Slider** for Target Temperature (`V1`).
   - Add a **Segmented Switch** for Mode (`V2`) and Fan Speed (`V3`).
   - Add a **Value Display** for Room Temperature (`V5`).
   - Add a **Button / Switch** for Display Light (`V4`) and Vertical Swing (`V6`).

---

## 5. Setting up Apple Siri Shortcuts

1. Open the **Shortcuts** app on your iPhone.
2. Tap **+** (New Shortcut) $\to$ Name it *"Turn On AC"*.
3. Add action: **Get Contents of URL**:
   - URL:
     ```text
     https://blynk.cloud/external/api/update?token=YOUR_AUTH_TOKEN&v0=1
     ```
   - Method: `GET`
4. Create another for *"Turn Off AC"*:
   - URL:
     ```text
     https://blynk.cloud/external/api/update?token=YOUR_AUTH_TOKEN&v0=0
     ```
5. Create one for *"Set AC 24"*:
   - URL:
     ```text
     https://blynk.cloud/external/api/update?token=YOUR_AUTH_TOKEN&v1=24
     ```
6. Now you can say *"Hey Siri, Turn On AC"* or add these shortcuts as widgets on your iPhone Home Screen and Lock Screen!

---

## 6. Wireless (OTA) Updates

Once you have flashed the ESP32 once via USB, you can update firmware **wirelessly over Wi-Fi** without disconnecting the ESP32 from the AC!

### In Arduino IDE:
1. Ensure your PC is connected to the same Wi-Fi network as the ESP32 (`Bsnl fiber net 2.4`).
2. Go to **Tools $\to$ Port**.
3. Under **Network Ports**, select `bluestar-ac at <ESP32-IP>`.
4. Click **Upload**.

### In PlatformIO:
1. Open `platformio.ini`.
2. Uncomment the OTA lines:
   ```ini
   upload_protocol = espota
   upload_port = bluestar-ac.local  ; or your ESP32's IP address
   ```
3. Run `pio run -t upload`.

---

## 7. Telnet Diagnostic Console (Port 23)

The firmware includes a lightweight, built-in Telnet server running on port 23. You can stream serial debug logs wirelessly over Wi-Fi without having a USB cable connected.

### Connecting to Telnet:
Use PuTTY, `nc`, or standard Telnet:
```bash
# Windows PowerShell / CMD or Linux/macOS Terminal:
telnet 192.168.1.59 23
# Or using Netcat:
nc 192.168.1.59 23
```

### Interactive Telnet Commands:
Once connected, send any of these single-key commands:
- **`q` or `Q`**: Query Extended Diagnostics. Reads Compressor Frequency (Key 24), Coil Temperature (Key 62), Operating Profile (Key 29), Lifetime Run Hours (Keys 43/44/59/60), and Hardware ID (Key 61).
- **`s` or `S`**: Send a manual Tuya keep-alive heartbeat (`CMD_HEARTBEAT 0x00`).
- **`h` or `H`**: Trigger full Tuya initialization handshake (`CMD_PRODUCT_QUERY`).
- **`r` or `R`**: Reboot ESP32.

### Python Headless Diagnostic Tool:
You can also run the provided script to query and view real-time diagnostics in a single command:
```bash
python scripts/query_diag.py
```

---

## 8. Critical Gotchas & Troubleshooting

1. **DevKit V1 Pinout Gotcha (RX0/TX0 vs RX2/TX2):**
   - **Do NOT** connect the AC to `RX0` (GPIO 3) or `TX0` (GPIO 1). On ESP32 DevKit V1, these pins are tied directly to the onboard CP2102/CH340 USB chip. Connecting to them causes bus contention, resulting in `Total RX: 0 bytes`.
   - **Always use Hardware UART2**: `GPIO 16 (RX2)` and `GPIO 17 (TX2)`.

2. **The `pinMode()` Detach Trap in ESP32 Arduino Core:**
   - **Never call `pinMode(AC_RX_PIN, ...)` after `acSerial.begin()`!**
   - In the ESP32 Arduino core, calling `pinMode()` on a hardware UART pin detaches the internal GPIO matrix from the UART peripheral, permanently muting incoming serial data. If your ESP32 registers zero RX bytes despite correct wiring, check that no `pinMode()` call touches GPIO 16.

3. **Understanding AC Beeps & Buzzer Mechanics:**
   - The Blue Star indoor unit buzzer is wired directly to Tuya MCU DP writes (`CMD_DP_SET 0x06`). **Every write command causes an audible chime.**
   - Do **NOT** set automated periodic background timers that write to the AC (such as querying Key 24/62 every minute), or the AC will beep constantly on schedule.
   - The firmware uses native Tuya `CMD_HEARTBEAT (0x00)` every 15 seconds for link keepalive, which the AC acknowledges **100% silently**.
   - Compressor frequency (`V17`) and coil temperature (`V18`) are updated whenever the AC pushes changes, or on-demand via the **`V19`** button or Telnet `q`.

4. **Never Connect USB while Powered by AC 5V:**
   - ESP32 DevKit boards lack ideal reverse-voltage protection between the 5V/VIN header and USB VBUS. Having both connected simultaneously risks frying the ESP32 or damaging your computer's USB port.
   - Always disconnect the AC 5V line before connecting USB, or update firmware wirelessly using **OTA** (Over-The-Air) on Port 3232.
