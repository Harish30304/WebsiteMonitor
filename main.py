import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL_TO_CHECK = "https://nextstep.tcs.com/"
STATE_FILE = "last_status.txt"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to send Telegram message: {e}")
        return None

def check_website():
    try:
        response = requests.get(URL_TO_CHECK, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Read last status
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        last_status = f.read().strip()
else:
    last_status = "UP"  # assume UP initially

# Check current status
website_up = check_website()
current_status = "UP" if website_up else "DOWN"

# Send message if status changed
if current_status != last_status:
    msg = f"✅ Website is UP: {URL_TO_CHECK}" if website_up else f"❌ Website is DOWN: {URL_TO_CHECK}"
    print(msg)
    send_telegram_message(msg)

# Update state file
with open(STATE_FILE, "w") as f:
    f.write(current_status)
