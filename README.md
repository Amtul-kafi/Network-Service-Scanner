markdown
# 🔍 Network Service Scanner

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

> A fast, multi‑threaded TCP/UDP scanner with service detection, banner grabbing, logging, and multi‑format reports.

---

## ✨ Features

| Category | Details |
|----------|---------|
| **Protocols** | TCP connect scanning + UDP probing |
| **Detection** | Service identification + banner grabbing |
| **Performance** | Multi‑threaded with progress bar |
| **Output** | Markdown, JSON, CSV reports + activity log |
| **User experience** | Colourful terminal, verbose mode |

---

## 📦 Installation

```bash
git clone https://github.com/Amtul-kafi/Network-Service-Scanner.git
cd Network-Service-Scanner
pip install -r requirements.txt
🚀 Usage
Basic TCP scan
bash
py main.py -t scanme.nmap.org -p 22,80,443 -v
UDP scan
bash
py main.py -t scanme.nmap.org -p 53,123,161 -u -v
Full scan with JSON report
bash
py main.py -t 192.168.1.1 -p 1-1000 -T 200 -o json
⚙️ Command Line Arguments
Argument	Description
-t, --target	Target IP or hostname
-p, --ports	Port range (e.g. 22,80 or 1-1000)
-T, --threads	Number of threads (default: 100)
-v, --verbose	Show detailed output
--timeout	Socket timeout in seconds
-o, --output	Report format: markdown, json, csv
-u, --udp	Enable UDP scanning
--no-banner	Disable banner grabbing (faster)
--no-service	Disable service detection (faster)
🖼️ Example Output
https://Screenshot.png

📄 License
MIT © Amtul Kafi

text

## Why this looks better:

- **Badges** at the top (Python version, license, platform) – professional and informative
- **Clean emojis** for section headers (🔍, ✨, 📦, 🚀, ⚙️, 🖼️, 📄)
- **Table for features** – more structured than bullet list
- **Clear separation** with horizontal rules (`---`)
- **Code blocks** with language tags for syntax highlighting
- **Compact layout** – easier to scan

## What to do:

1. Replace your `README.md` content with the block above
2. Save the file
3. Push to GitHub:
   ```powershell
   git add README.md
   git commit -m "docs: improve README formatting with badges and structure"
   git push origin main