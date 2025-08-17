# Internet Logger

Log your public IP, Speedtest (download/upload/ping), and first 5 traceroute hops to a CSV on Windows.

## What it does

- Runs Ookla Speedtest CLI in JSON mode and records:
  - Download (Mbps), Upload (Mbps), Ping (ms)
- Gets your current public IP from https://api.ipify.org
- Runs `tracert -d 8.8.8.8` and captures the first 5 hop IPs
- Appends a row to `internet_log.csv` with date/time and all values

CSV headers:

```
Date, Time, IP, Download_Mbps, Upload_Mbps, Ping_ms, Hop1, Hop2, Hop3, Hop4, Hop5
```

## Repo contents

- `internet_logger.py` — main script
- `internet_log.csv` — CSV log file (auto-created with headers if missing)
- `speedtest.exe` — Ookla Speedtest CLI (Windows) binary for convenience

## Requirements

- Windows (uses `tracert`)
- Python 3.8+
- Python package: `requests`
- Speedtest CLI available as `speedtest` on PATH or present as `speedtest.exe` in this folder

Install Python dependency:

```powershell
pip install requests
```

If you don’t have Speedtest CLI installed globally, the included `speedtest.exe` should work when you run the script from this folder. Otherwise, install it from Ookla and ensure `speedtest` is in your PATH.

## How to run

From this folder in PowerShell:

```powershell
python .\internet_logger.py
```

This will append one line to `internet_log.csv` and print a summary.

## Automate (optional)

Use Windows Task Scheduler to run periodically (e.g., every 15 minutes):

1. Open Task Scheduler → Create Basic Task
2. Trigger: Daily (then set repeat in Advanced)
3. Action: Start a program
   - Program/script: full path to `python.exe` (e.g., `C:\Users\You\AppData\Local\Programs\Python\Python39\python.exe`)
   - Add arguments: `C:\network-script\internet_logger.py`
   - Start in: `C:\network-script`
4. Finish → Open task Properties → Triggers → Edit → Repeat task every 15 minutes for a duration of 1 day → OK

## Troubleshooting

- "speedtest not found":
  - Keep `speedtest.exe` in this folder and run from here, or install Ookla Speedtest CLI and add it to PATH.
- SSL/firewall errors for IP lookup:
  - The script calls `https://api.ipify.org`; ensure outbound HTTPS is allowed.
- Empty traceroute hops:
  - Some networks/routers don’t respond to ICMP; blanks are expected.

## Notes

- Target for traceroute is `8.8.8.8` and max hops recorded is 5 (see `run_traceroute`).
- Speed conversion: the script converts Speedtest bandwidth (bytes/sec) to Mbps (megabits/sec).
- Data is appended; rotate/backup `internet_log.csv` as it grows.
