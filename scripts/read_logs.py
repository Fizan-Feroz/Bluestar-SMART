import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)
try:
    s.connect(('192.168.1.59', 23))
    print("[Connected to 192.168.1.59:23]")
    # Send power toggle command 'p'
    s.sendall(b'p\n')
    
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
