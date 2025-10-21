import requests
import time
import os

# Get credentials from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Website to monitor
URL_TO_CHECK = "https://nextstep.tcs.com/"

# Track current state
flag = True  # Assume website is up initially

def send_telegram_message(text):
    """Send a Telegram message via bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to send Telegram message: {e}")
        return None

def check_website():
    """Check if the website is reachable."""
    try:
        response = requests.get(URL_TO_CHECK, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Main monitoring loop
while True:
    website_up = check_website()
    if website_up and not flag:
        msg = f"✅ Website is UP: {URL_TO_CHECK}"
        print(msg)
        send_telegram_message(msg)
        flag = True
    elif not website_up and flag:
        msg = f"❌ Website is DOWN: {URL_TO_CHECK}"
        print(msg)
        send_telegram_message(msg)
        flag = False

    # Wait 1 minute before checking again
    time.sleep(60)
