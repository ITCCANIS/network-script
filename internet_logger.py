import csv
import datetime
import requests
import subprocess
import json

LOG_FILE = "internet_log.csv"

# Ensure CSV has headers if not already created
try:
    with open(LOG_FILE, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Date", "Time", "IP",
            "Download_Mbps", "Upload_Mbps", "Ping_ms",
            "Hop1", "Hop2", "Hop3", "Hop4", "Hop5"
        ])
except FileExistsError:
    pass

def run_speedtest():
    result = subprocess.run(["speedtest", "-f", "json"], capture_output=True, text=True)
    data = json.loads(result.stdout)

    download = round(data["download"]["bandwidth"] * 8 / 1e6, 2)  # Mbps
    upload = round(data["upload"]["bandwidth"] * 8 / 1e6, 2)      # Mbps
    ping = round(data["ping"]["latency"], 2)

    return download, upload, ping

def run_traceroute(target="8.8.8.8", max_hops=5):
    # Run Windows tracert
    result = subprocess.run(["tracert", "-d", target], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    hops = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2 and parts[0].isdigit():
            hops.append(parts[-1])  # last column = IP
        if len(hops) >= max_hops:
            break

    # Pad with blanks if fewer hops
    while len(hops) < max_hops:
        hops.append("")

    return hops

def log_data():
    ip = requests.get("https://api.ipify.org").text
    download, upload, ping = run_speedtest()
    hops = run_traceroute()

    now = datetime.datetime.now()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            now.date(), now.time().strftime("%H:%M:%S"), ip,
            download, upload, ping,
            *hops
        ])

    print(f"[{now}] IP={ip} | Down={download} Mbps | Up={upload} Mbps | Ping={ping} ms | Hops={hops}")

if __name__ == "__main__":
    log_data()
