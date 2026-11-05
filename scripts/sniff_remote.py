import socket
import time
import sys
import datetime

TARGET_IP = '192.168.1.59'
TARGET_PORT = 23
LOG_FILE = 'scripts/remote_sniff.log'

print(f"Connecting to ESP32 Telnet console at {TARGET_IP}:{TARGET_PORT}...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)

try:
    s.connect((TARGET_IP, TARGET_PORT))
    print(f"[Connected to {TARGET_IP}:{TARGET_PORT}] Logging to {LOG_FILE}...")
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(f"--- Sniff Session Started: {datetime.datetime.now()} ---\n")
        f.flush()
        
        while True:
            try:
                data = s.recv(1024)
                if data:
                    text = data.decode('utf-8', errors='replace')
                    sys.stdout.write(text)
                    sys.stdout.flush()
                    f.write(text)
                    f.flush()
            except socket.timeout:
                pass
except KeyboardInterrupt:
    print("\n[Sniffer stopped by user]")
except Exception as e:
    print(f"\n[Error]: {e}")
finally:
    s.close()
