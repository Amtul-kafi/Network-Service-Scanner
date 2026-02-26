# banner_grabber.py
import socket

def grab_banner(target, port, timeout=1):
    """
    Try to connect to the port and read banner
    Returns string banner or 'Unknown'
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((target, port))
        
        # Some services send banners automatically
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "Unknown"
        
        s.close()
        if banner == "":
            banner = "Unknown"
        return banner
    except Exception as e:
        return "Closed or filtered"