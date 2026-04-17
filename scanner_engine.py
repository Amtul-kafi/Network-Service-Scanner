import socket
import threading
from queue import Queue
from termcolor import colored
from tqdm import tqdm
from serviceDetect import detect_service
from banner_grabber import grab_banner

class ScannerEngine:
    def __init__(self, target_ip, ports, threads=100, timeout=1.0,
                 verbose=False, grab_banner=True, detect_service=True):
        self.target = target_ip
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        self.grab_banner = grab_banner
        self.detect_service = detect_service
        self.results = []
        self.lock = threading.Lock()
        self.queue = Queue()

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                state = "open"
                banner = None
                service = None
                if self.grab_banner:
                    banner = grab_banner(self.target, port, self.timeout)
                if self.detect_service:
                    service = detect_service(port, banner)
                if self.verbose:
                    print(colored(f"[+] Port {port} is OPEN | Service: {service}", "green"))
            else:
                state = "closed"
                service = None
                banner = None
                if self.verbose:
                    print(colored(f"[-] Port {port} is closed", "red"))
            with self.lock:
                self.results.append({"port": port, "state": state, "service": service, "banner": banner})
        except Exception as e:
            if self.verbose:
                print(colored(f"[!] Error scanning port {port}: {e}", "yellow"))

    def worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            self.scan_port(port)
            self.queue.task_done()

    def run(self):
        print(colored(f"\n[*] Starting scan on target: {self.target}", "cyan"))
        print(colored(f"[*] Ports to scan: {len(self.ports)} ports", "cyan"))
        print(colored(f"[*] Threads: {self.threads}", "cyan"))
        print(colored(f"[*] Timeout: {self.timeout}s", "cyan"))
        print(colored("-" * 50, "cyan"))

        for port in self.ports:
            self.queue.put(port)

        thread_list = []
        for _ in range(min(self.threads, len(self.ports))):
            t = threading.Thread(target=self.worker)
            t.start()
            thread_list.append(t)

        with tqdm(total=len(self.ports), desc="Scanning ports", unit="port") as pbar:
            while any(t.is_alive() for t in thread_list):
                pbar.update(self.queue.qsize())
                threading.Event().wait(0.5)
            pbar.update(len(self.ports) - pbar.n)

        for t in thread_list:
            t.join()

        print(colored("\n[+] Scan completed!", "green"))
        return self.results
