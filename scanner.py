import socket
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.serviceDetect import detect_service
from core.report import ReportManager

print("==== ScanopyB Professional TCP Scanner ====")

# ---------------------------
# INPUT
# ---------------------------
target = input("Enter target IP (e.g., 127.0.0.1): ").strip()
port_input = input("Enter ports (e.g., 22,80,443 or 1-1024): ").strip()


# ---------------------------
# PORT PARSER
# ---------------------------
def parse_ports(port_str):
    ports = set()

    if "-" in port_str:
        start, end = port_str.split("-")
        for p in range(int(start), int(end) + 1):
            ports.add(p)

    elif "," in port_str:
        for p in port_str.split(","):
            ports.add(int(p.strip()))

    else:
        ports.add(int(port_str))

    return sorted(ports)


if not port_input:
    ports = list(range(1, 1025))
else:
    try:
        ports = parse_ports(port_input)
    except:
        print("Invalid port format.")
        exit()


# ---------------------------
# BANNER GRABBER
# ---------------------------
def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))

        # HTTP detection
        if port in [80, 8080, 8000, 8888]:
            req = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            s.send(req.encode())
            response = s.recv(4096).decode(errors="ignore")

            for line in response.split("\r\n"):
                if "Server:" in line:
                    return line.strip()

            return "HTTP service detected"

        banner = s.recv(1024).decode(errors="ignore").strip()

        return banner if banner else "No banner"

    except:
        return None

    finally:
        try:
            s.close()
        except:
            pass


# ---------------------------
# SCAN FUNCTION
# ---------------------------
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        if s.connect_ex((target, port)) == 0:
            service = detect_service(port)
            banner = grab_banner(target, port)

            return (port, service, banner)

    except:
        pass

    return None


# ---------------------------
# EXECUTION
# ---------------------------
print(f"\nScanning {target} ({len(ports)} ports)...\n")

start_time = datetime.datetime.now()
open_ports = []

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(scan_port, port) for port in ports]

    for future in as_completed(futures):
        result = future.result()

        if result:
            port, service, banner = result

            if banner:
                print(f"[+] Port {port} OPEN → {service} → {banner}")
            else:
                print(f"[+] Port {port} OPEN → {service}")

            open_ports.append((port, service, banner))

end_time = datetime.datetime.now()
duration = (end_time - start_time).total_seconds()

print("\nScan complete!")
print(f"Scan duration: {duration:.2f} seconds")


# ---------------------------
# REPORTING (PROPER WAY)
# ---------------------------
reporter = ReportManager()
reporter.save(target, ports, open_ports, duration)