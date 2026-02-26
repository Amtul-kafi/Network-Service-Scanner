import socket
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

print("==== ScanopyB Professional TCP Scanner ====")

target = input("Enter target IP (e.g., 127.0.0.1): ").strip()
port_input = input("Enter ports (e.g., 22,80,443 or 1-1024): ").strip()

# ---------------------------
# Port Parsing
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

if port_input == "":
    ports = list(range(1, 1025))
else:
    try:
        ports = parse_ports(port_input)
    except:
        print("Invalid port format.")
        exit()

# ---------------------------
# Banner Grabber
# ---------------------------
def grab_banner(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((target, port))

        # ---------------------------
        # HTTP detection
        # ---------------------------
        if port in [80, 8080, 8000, 8888]:
            http_request = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
            s.send(http_request.encode())
            response = s.recv(4096).decode(errors="ignore")

            # Extract Server header if present
            for line in response.split("\r\n"):
                if "Server:" in line:
                    s.close()
                    return line.strip()

            s.close()
            return "HTTP service detected"

        # ---------------------------
        # Default banner grabbing
        # ---------------------------
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()

        if banner:
            return banner
        else:
            return "No banner"

    except:
        return None
# ---------------------------
# Port Scan Function
# ---------------------------
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        s.close()
        if result == 0:
            banner = grab_banner(target, port)
            return (port, banner)
    except:
        return None
    return None

# ---------------------------
# Scan Execution
# ---------------------------
print(f"\nScanning {target} ({len(ports)} ports)...\n")

start_time = datetime.datetime.now()
open_ports = []

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(scan_port, port) for port in ports]
    for future in as_completed(futures):
        result = future.result()
        if result:
            port, banner = result
            print(f"[+] Port {port} OPEN → {banner}")
            open_ports.append((port, banner))

end_time = datetime.datetime.now()
duration = (end_time - start_time).total_seconds()

print("\nScan complete!")
print(f"Scan duration: {duration:.2f} seconds")

# ---------------------------
# Save Report
# ---------------------------
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_name = f"scan_{target.replace('.', '_')}.md"

report_lines = [
    "# ScanopyB Professional Scan Report",
    f"Target: {target}",
    f"Timestamp: {timestamp}",
    f"Total Ports Scanned: {len(ports)}",
    f"Scan Duration: {duration:.2f} seconds",
    "",
    "## Open Ports and Services"
]

if open_ports:
    for port, banner in open_ports:
        report_lines.append(f"- Port {port}: {banner}")
else:
    report_lines.append("No open ports found.")

# Create reports folder if not exists
import os
if not os.path.exists("reports"):
    os.makedirs("reports")

with open(f"reports/{report_name}", "w") as f:
    for line in report_lines:
        f.write(line + "\n")

print(f"Report saved to reports/{report_name}")