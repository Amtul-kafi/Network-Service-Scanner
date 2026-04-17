import os
from datetime import datetime

class ReportManager:

    def __init__(self, base_folder="reports"):
        self.base_folder = base_folder
        self.history_folder = os.path.join(base_folder, "history")
        os.makedirs(self.history_folder, exist_ok=True)

    def save(self, target, ports, open_ports, duration):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        history_file = os.path.join(
            self.history_folder,
            f"scan_{target.replace('.', '_')}_{timestamp}.md"
        )

        latest_file = os.path.join(self.base_folder, "latest_scan.md")

        content = self._build_report(target, ports, open_ports, duration, timestamp)

        # history (never overwritten)
        with open(history_file, "w") as f:
            f.write(content)

        # latest (always overwritten)
        with open(latest_file, "w") as f:
            f.write(content)

        print(f"[✓] Latest report updated")
        print(f"[✓] History saved")

    def _build_report(self, target, ports, open_ports, duration, timestamp):
        lines = []
        lines.append("# Scan Report\n")
        lines.append(f"Target: {target}")
        lines.append(f"Time: {timestamp}")
        lines.append(f"Ports scanned: {len(ports)}")
        lines.append(f"Duration: {duration:.2f}s\n")

        lines.append("## Open Ports")

        if open_ports:
            for port, service, banner in open_ports:
                if banner:
                    lines.append(f"- {port} → {service} | {banner}")
                else:
                    lines.append(f"- {port} → {service}")
        else:
            lines.append("No open ports found")

        return "\n".join(lines)