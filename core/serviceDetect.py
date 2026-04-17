def detect_service(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "TELNET",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        139: "NETBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MYSQL",
        3389: "RDP",
        8080: "HTTP-ALT"
    }

    return services.get(port, "Unknown Service")