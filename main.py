import requests
import os
from dotenv import load_dotenv
from google import genai
import yfinance as yf
import schedule
import time

load_dotenv()

print("GEMINI:", os.getenv("GEMINI_API_KEY"))

# ===== ENV =====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ===== GEMINI =====
client = genai.Client(api_key=GEMINI_API_KEY)


# ===== PRICE DATA =====
def get_news():
    tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
    results = []

    for t in tickers:
        data = yf.Ticker(t).history(period="1d")

        if data.empty:
            continue

        price = data["Close"].iloc[-1]

        results.append({
            "title": f"{t} price sekarang: ${price:.2f}"
        })

    return results


# ===== AI ANALYSIS =====
def analyze(title):
    prompt = f"""
Kamu adalah crypto analyst profesional.

Data market:
{title}

Berikan analisa singkat dengan format:

🚨 MARKET UPDATE
🧠 Sentiment: bullish / bearish / neutral
📊 Impact: apa arti movement ini
🎯 Insight: apa yang perlu diperhatikan trader
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# ===== SEND TELEGRAM =====
def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
    )



# ===== RUN BOT =====
def run():
    news_list = get_news()

    print("Found:", len(news_list), "coins")

    for news in news_list:
        title = news["title"]

        print("Processing:", title)

        result = analyze(title)

        print(result)

        send(result)

# ===== AUTO SCHEDULE =====
schedule.every(15).minutes.do(run)

print("🚀 Crypto AI bot running every 15 minutes...")

run()  # langsung jalan pertama kali

while True:
    schedule.run_pending()
    time.sleep(5)
