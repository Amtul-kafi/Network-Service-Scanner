import argparse
from utils import parse_ports

def get_arguments():
    parser = argparse.ArgumentParser(
        description="Advanced Port Scanner with Service Detection & Banner Grabbing",
        epilog="Example: python main.py -t 192.168.1.1 -p 20-1000 -v"
    )
    parser.add_argument("-t", "--target", required=True,
                        help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range to scan (e.g., 22,80,443,1000-2000). Default: 1-1024")
    parser.add_argument("-T", "--threads", type=int, default=100,
                        help="Number of threads for scanning (default: 100)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--timeout", type=float, default=1.0,
                        help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("-o", "--output", choices=['markdown', 'json', 'csv'], default='markdown',
                        help="Report output format (default: markdown)")
    parser.add_argument("--no-banner", action="store_true",
                        help="Disable banner grabbing (faster scan)")
    parser.add_argument("--no-service", action="store_true",
                        help="Disable service detection (faster scan)")
    
    # UDP scan flag
    parser.add_argument("-u", "--udp", action="store_true",
                        help="Enable UDP scanning (TCP is default)")

    args = parser.parse_args()
    args.ports = parse_ports(args.ports)
    return args