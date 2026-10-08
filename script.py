import socket
import requests


print("[+] Make ur comfortable and easy CTFs")

Target_IP = input("add ur IP: ").strip()
open_ports_list = []


http_ports = [80, 8080, 8888, 4444, 8083, 443]

def scan_ports(ip, ports_to_check):
    print(f"\n[*] Scanning {ip}...")
    for port in ports_to_check:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((ip, int(port)))
            print(f"[+] Port {port} OPEN")
            open_ports_list.append(int(port))
            s.close()
        except:
            pass
    return open_ports_list

# Function of http enumeration
def http_enum(url):
    print(f"\n[I] http enum on {url}")
    try:
        r = requests.get(f"{url}/robots.txt", timeout=3)
        if r.status_code == 200:
            print(f"[+] Found robots.txt:\n{r.text}")
    except:
        pass

    # 2.  brute force on the hidden directories
    wordlist = ["admin", "login", "dashboard", "config", "backup", "uploads", "secret"]
    print("[*] Bruteforcing hidden dirs...")
    for path in wordlist:
        try:
            full_url = f"{url}/{path}"
            r = requests.get(full_url, timeout=2)
            if r.status_code!= 404:
                print(f" -> Found: {full_url} [{r.status_code}]")
        except:
            pass

# --- Main ---
ports_input = input("add ur open ports (ex: 22,80,443): ")
ports = [p.strip() for p in ports_input.split(",")]

scanned = scan_ports(Target_IP, ports)

for port in scanned:
    if port in http_ports:
        print(f"\n[->] Port {port} is HTTP, starting http_enum")
        if port == 80:
            url = f"http://{Target_IP}"
        else:
            url = f"http://{Target_IP}:{port}"
        http_enum(url)
