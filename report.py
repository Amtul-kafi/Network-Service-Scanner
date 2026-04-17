import json
import csv
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, target, results, output_format="markdown"):
        self.target = target
        self.results = results
        self.format = output_format
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate(self):
        if self.format == "markdown":
            return self._markdown()
        elif self.format == "json":
            return self._json()
        elif self.format == "csv":
            return self._csv()
        else:
            raise ValueError(f"Unsupported format: {self.format}")

    def _markdown(self):
        filename = f"reports/scan_{self.target}_{self.timestamp}.md"
        os.makedirs("reports", exist_ok=True)
        with open(filename, "w") as f:
            f.write(f"# Port Scan Report\n\n")
            f.write(f"**Target:** {self.target}\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Open Ports\n\n")
            f.write("| Port | Service | Banner |\n")
            f.write("|------|---------|--------|\n")
            for res in self.results:
                if res["state"] == "open":
                    banner = (res["banner"][:50] + "...") if res["banner"] and len(res["banner"]) > 50 else res["banner"]
                    f.write(f"| {res['port']} | {res['service']} | {banner or ''} |\n")
            if not any(r["state"] == "open" for r in self.results):
                f.write("No open ports found.\n")
        return filename

    def _json(self):
        filename = f"reports/scan_{self.target}_{self.timestamp}.json"
        os.makedirs("reports", exist_ok=True)
        data = {
            "target": self.target,
            "timestamp": self.timestamp,
            "results": [r for r in self.results if r["state"] == "open"]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return filename

    def _csv(self):
        filename = f"reports/scan_{self.target}_{self.timestamp}.csv"
        os.makedirs("reports", exist_ok=True)
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Port", "State", "Service", "Banner"])
            for res in self.results:
                writer.writerow([res["port"], res["state"], res["service"], res["banner"]])
        return filename

