import requests, json

def send_telegram_alert(down_sites):
    with open('config.json') as f:
        config = json.load(f)
    token = config["alert"]["telegram_bot_token"]
    chat_id = config["alert"]["chat_id"]
    message = "🚨 The following sites are DOWN:\n" + "\n".join(f"🔴 {url}" for url in down_sites)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})