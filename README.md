# Advanced Port Scanner

A fast, multi‑threaded port scanner with service detection, banner grabbing, and UDP support.  
Built with Python for ethical network reconnaissance.

## Features

- TCP connect scanning (multi‑threaded)
- UDP scanning (with open/filtered detection)
- Service detection (maps ports to common services)
- Banner grabbing (extracts service banners)
- Report generation: Markdown, JSON, CSV
- Verbose mode and progress bar
- Colourful terminal output

## Why I built this

I wanted to understand how tools like Nmap work under the hood. This project taught me about sockets, threading, network protocols, and how to structure a Python project.

## Installation

```bash
git clone https://github.com/Amtul-kafi/PortScanner_project.git
cd PortScanner_project
pip install -r requirements.txt