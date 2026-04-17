# Network Service Scanner

A multi-threaded TCP/UDP port scanner with service detection, banner grabbing, logging, and report generation. Built for learning network security and authorised reconnaissance.

## Features

- TCP connect scanning (multi-threaded)
- UDP scanning (open/filtered detection)
- Service detection (maps ports to common services)
- Banner grabbing (extracts service banners)
- Report generation: Markdown, JSON, CSV
- Activity logging to file (scanner.log)
- Verbose mode with real-time output
- Colourful terminal output with progress bar

## Installation

git clone https://github.com/Amtul-kafi/Network-Service-Scanner.git
cd Network-Service-Scanner
pip install -r requirements.txt

## Usage

TCP scan:
py main.py -t scanme.nmap.org -p 22,80,443 -v

UDP scan:
py main.py -t scanme.nmap.org -p 53,123,161 -u -v

Full scan with JSON report:
py main.py -t 192.168.1.1 -p 1-1000 -T 200 -o json

## Arguments

-t, --target : Target IP or hostname
-p, --ports   : Port range (e.g. 22,80,443 or 1-1000)
-T, --threads : Number of threads (default: 100)
-v, --verbose : Show detailed output
--timeout     : Socket timeout in seconds
-o, --output  : Report format: markdown, json, csv
-u, --udp     : Enable UDP scanning
--no-banner   : Disable banner grabbing (faster)
--no-service  : Disable service detection (faster)

## Example output

[Screenshot given] 

## License

MIT

## Author

Amtul Kafi
https://github.com/Amtul-kafi