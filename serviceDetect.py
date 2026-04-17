def detect_service(port, banner=""):
    common_services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC",
        135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
        445: "SMB", 993: "IMAPS", 995: "POP3S", 1723: "PPTP",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
        6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
    }
    service = common_services.get(port, "Unknown")
    if banner:
        banner_lower = banner.lower()
        if "ssh" in banner_lower:
            service = "SSH"
        elif "ftp" in banner_lower:
            service = "FTP"
        elif "http" in banner_lower:
            service = "HTTP"
        elif "mysql" in banner_lower:
            service = "MySQL"
    return service
