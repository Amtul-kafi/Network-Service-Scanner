import socket
import os

def validate_ip(ip):
    """Check if the given string is a valid IPv4 address."""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def resolve_hostname(hostname):
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def parse_ports(port_string):
    """
    Parse port string like "22,80,100-200,443"
    Returns a list of integers.
    """
    ports = set()
    parts = port_string.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def is_privileged():
    """Check if script is run with admin/root privileges."""
    try:
        return os.getuid() == 0
    except AttributeError:
        # Windows: assume admin (or handle differently)
        return True