import subprocess, json, datetime, csv, requests

LOG_FILE = "internet_log.csv"

try:
    with open(LOG_FILE, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Time", "IP", "Download_Mbps", "Upload_Mbps", "Ping_ms"])
except FileExistsError:
    pass

def log_speed():
    # Get IP
    ip = requests.get("https://api.ipify.org").text

    # Run Ookla speedtest in JSON mode
    result = subprocess.run(["speedtest", "-f", "json"], capture_output=True, text=True)
    data = json.loads(result.stdout)

    download = round(data["download"]["bandwidth"] * 8 / 1e6, 2)  # to Mbps
    upload = round(data["upload"]["bandwidth"] * 8 / 1e6, 2)
    ping = round(data["ping"]["latency"], 2)

    now = datetime.datetime.now()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now.date(), now.time().strftime("%H:%M:%S"), ip, download, upload, ping])

    print(f"[{now}] IP={ip} | Down={download} Mbps | Up={upload} Mbps | Ping={ping} ms")

if __name__ == "__main__":
    log_speed()
