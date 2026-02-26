# utils.py
import os

def save_report(filename, lines):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    with open(f"reports/{filename}", "w") as f:
        f.write("\n".join(lines))