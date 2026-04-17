import socket

def grab_banner(ip, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.send(b"\r\n")
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner if banner else None
    except:
        return None
