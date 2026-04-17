import socket
from termcolor import colored

def udp_scan(target_ip, port, timeout=2):
    """
    Scan a single UDP port.
    Returns True if likely open, False if closed, None if open|filtered.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        # Send an empty probe (some services respond)
        sock.sendto(b'\x00\x00', (target_ip, port))
        # Try to receive a response
        data, addr = sock.recvfrom(1024)
        sock.close()
        if data:
            return True
    except socket.timeout:
        # No response doesn't necessarily mean closed – UDP is unreliable
        return None
    except ConnectionRefusedError:
        # ICMP port unreachable – definitely closed
        return False
    except Exception:
        pass
    return None

def scan_udp_ports(target_ip, ports, verbose=False, timeout=2):
    """
    Scan a list of UDP ports.
    Returns list of ports that are open or open|filtered.
    """
    results = []
    for port in ports:
        status = udp_scan(target_ip, port, timeout)
        if status is True:
            results.append(port)
            if verbose:
                print(colored(f"[+] UDP Port {port} is OPEN", "green"))
        elif status is None:
            # open|filtered – still worth noting
            results.append(port)
            if verbose:
                print(colored(f"[?] UDP Port {port} is OPEN|FILTERED", "yellow"))
        else:
            if verbose:
                print(colored(f"[-] UDP Port {port} is CLOSED", "red"))
    return results