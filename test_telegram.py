import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

res = requests.post(url, json={
    "chat_id": CHAT,
    "text": "🔥 Test dari Crypto AI bot"
})

print(res.text)
