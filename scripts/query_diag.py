import socket
import sys
import time

TARGET_IP = sys.argv[1] if len(sys.argv) > 1 else '192.168.1.59'
TARGET_PORT = 23

print(f"Connecting to ESP32 Telnet console at {TARGET_IP}:{TARGET_PORT}...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)
try:
    s.connect((TARGET_IP, TARGET_PORT))
    print(f"[Connected to {TARGET_IP}:{TARGET_PORT}]")
    print("Triggering extended diagnostics query ('q')...\n")
    # Send 'q' to query all extended diagnostics
    s.sendall(b'q\n')
    
    start = time.time()
    while time.time() - start < 10.0:
        try:
            data = s.recv(1024)
            if data:
                print(data.decode('utf-8', errors='replace'), end='', flush=True)
        except socket.timeout:
            pass
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
    print("\n[Connection closed]")
