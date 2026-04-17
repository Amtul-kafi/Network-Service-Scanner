#!/usr/bin/env python3
"""
Port Scanner Project - Main Entry Point
Author: Amtul Kafi
License: MIT
"""

import sys
from termcolor import colored
from parser import get_arguments
from scanner_engine import ScannerEngine
from report import ReportGenerator
from logger import setup_logger
from utils import resolve_hostname, validate_ip, is_privileged

def main():
    # Display banner
    print(colored("""
    ╔══════════════════════════════════════╗
    ║     Advanced Port Scanner v1.0       ║
    ║        by Amtul Kafi                 ║
    ╚══════════════════════════════════════╝
    """, "blue"))

    # Ethical warning
    print(colored("[!] WARNING: Use this tool only on networks you own or have explicit permission to scan.", "yellow"))
    print(colored("[!] Unauthorized scanning may be illegal in your jurisdiction.\n", "yellow"))

    # Parse arguments
    args = get_arguments()

    # Setup logger
    logger = setup_logger()
    logger.info("Starting Port Scanner")

    # Resolve hostname
    if validate_ip(args.target):
        target_ip = args.target
    else:
        logger.info(f"Resolving hostname: {args.target}")
        target_ip = resolve_hostname(args.target)
        if not target_ip:
            print(colored(f"[-] Could not resolve hostname: {args.target}", "red"))
            sys.exit(1)
        print(colored(f"[+] Resolved {args.target} -> {target_ip}", "green"))

    # Privilege check 
    if any(p < 1024 for p in args.ports) and not is_privileged():
        print(colored("[!] Scanning ports below 1024 may require root/administrator privileges.", "yellow"))

    # Initialize TCP scanner
    scanner = ScannerEngine(
        target_ip=target_ip,
        ports=args.ports,
        threads=args.threads,
        timeout=args.timeout,
        verbose=args.verbose,
        grab_banner=not args.no_banner,
        detect_service=not args.no_service
    )

    # Run TCP scan
    try:
        results = scanner.run()
    except KeyboardInterrupt:
        print(colored("\n[!] Scan interrupted by user.", "red"))
        logger.info("Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(colored(f"\n[!] Fatal error: {e}", "red"))
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

    # Generate report 
    report_gen = ReportGenerator(target_ip, results, output_format=args.output)
    report_file = report_gen.generate()
    print(colored(f"\n[+] Report saved to: {report_file}", "green"))

    # Print summary of TCP open ports
    open_ports = [r for r in results if r["state"] == "open"]
    if open_ports:
        print(colored("\n[+] TCP open ports found:", "green"))
        for p in open_ports:
            print(f"    {p['port']}/tcp - {p['service']}")
    else:
        print(colored("\n[-] No TCP open ports found.", "yellow"))

    # ---------- UDP SCAN ----------
    if args.udp:
        from udp_scanner import scan_udp_ports
        print(colored("\n[*] Starting UDP scan...", "cyan"))
        udp_open = scan_udp_ports(target_ip, args.ports, args.verbose, args.timeout)
        if udp_open:
            print(colored("[+] UDP open ports found:", "green"))
            for p in udp_open:
                print(f"    {p}/udp")
            # Optionally append UDP results to the report
           
        else:
            print(colored("[-] No open UDP ports found (or all filtered).", "yellow"))

    logger.info("Scan completed successfully")

if __name__ == "__main__":
    main()