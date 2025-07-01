import requests, time, json, os
from datetime import datetime
from alert import send_telegram_alert

def load_config():
    with open('config.json') as f:
        return json.load(f)

def log_status(url, status, response_time):
    os.makedirs("logs", exist_ok=True)
    with open('logs/history.csv', 'a') as f:
        now = datetime.now().isoformat()
        f.write(f"{now},{url},{status},{response_time}\n")

def is_up(url, timeout):
    try:
        start = time.time()
        r = requests.get(url, timeout=timeout)
        duration = round(time.time() - start, 2)
        return r.status_code == 200, duration
    except:
        return False, None

def main():
    config = load_config()
    down_sites = []

    for url in config["urls"]:
        success = False
        response_time = None
        for _ in range(config["retry_attempts"]):
            success, response_time = is_up(url, config["timeout_seconds"])
            if success:
                break
            time.sleep(1)
        status = "UP" if success else "DOWN"
        log_status(url, status, response_time if response_time else "N/A")
        if status == "DOWN":
            down_sites.append(url)

    if down_sites:
        send_telegram_alert(down_sites)

if __name__ == "__main__":
    main()