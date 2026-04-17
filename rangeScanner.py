# rangeScanner.py

import socket
from datetime import datetime
import os

# ---------- CONFIG ----------
TIMEOUT = 0.5
REPORT_FOLDER = "reports"


# ---------- HELPER: Parse Ports ----------
def parse_ports(port_input):
    ports = []
    if "-" in port_input:
        start, end = port_input.split("-")
        ports = list(range(int(start), int(end) + 1))
    else:
        ports = [int(p.strip()) for p in port_input.split(",") if p.strip().isdigit()]
    return ports


# ---------- HELPER: Banner Grab ----------
def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(TIMEOUT)
        sock.connect((ip, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner.split("\n")[0]
    except:
        return "No banner"


# ---------- PORT SCAN ----------
def scan_ports(ip, ports):
    open_ports = []

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            result = sock.connect_ex((ip, port))

            if result == 0:
                print(f"[+] {ip}:{port} OPEN")
                banner = grab_banner(ip, port)
                open_ports.append((port, banner))

            sock.close()

        except:
            continue

    return open_ports


# ---------- REPORT GENERATION ----------
def save_report(ip, ports_scanned, open_ports, duration):
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{REPORT_FOLDER}/scan_{ip}_{timestamp}.md"

    with open(filename, "w") as f:
        f.write("# ScanopyB Range Scan Report\n\n")
        f.write(f"**Target:** {ip}\n")
        f.write(f"**Timestamp:** {timestamp}\n")
        f.write(f"**Total Ports Scanned:** {len(ports_scanned)}\n")
        f.write(f"**Scan Duration:** {duration:.2f} seconds\n\n")

        f.write("## Open Ports and Services\n")

        if open_ports:
            for port, banner in open_ports:
                f.write(f"- **Port {port}** → {banner}\n")
        else:
            f.write("No open ports found.\n")

    print(f"[✓] Report saved: {filename}")


# ---------- MAIN ----------
def main():
    print("==== ScanopyB Professional Range Scanner ====")

    target_base = input("Enter base IP (e.g., 192.168.1): ").strip()
    start_host = int(input("Start host (e.g., 1): ").strip())
    end_host = int(input("End host (e.g., 5): ").strip())
    port_input = input("Enter ports (e.g., 22,80,443 or 1-1024): ").strip()

    ports = parse_ports(port_input)

    for host in range(start_host, end_host + 1):
        ip = f"{target_base}.{host}"

        print(f"\nScanning {ip} ({len(ports)} ports)...")

        start_time = datetime.now()
        open_ports = scan_ports(ip, ports)
        end_time = datetime.now()

        duration = (end_time - start_time).total_seconds()

        save_report(ip, ports, open_ports, duration)


if __name__ == "__main__":
    main()