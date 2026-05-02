import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask
from threading import Thread

# --- تنظیمات شما ---
TOKEN = '8740696167:AAHSCQete8X7EMDVcFovV9RBjaJnMy-KEJA'
CHAT_ID = '391754544'
WALLET = 'UQDo6vfO8kdvGNATer9nsTEki3ljoGLKoHmS2opGsafmSwxj'

app = Flask('')

@app.route('/')
def home():
    return "<h1>Bot is Active!</h1>"

def run():
    # Render به پورت 10000 نیاز دارد
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def send_telegram(msg):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    try:
        res = requests.post(url, json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'}, timeout=20)
        print(f"--- STATUS TELEGRAM: {res.status_code} ---")
        print(f"--- RESPONSE: {res.text} ---")
        return res.status_code == 200
    except Exception as e:
        print(f"--- ERROR: {e} ---")
        return False

def check_airdrops():
    print("Checking site...")
    # کد اسکرپر (ساده شده برای تست)
    send_telegram(f"🔍 ربات در حال چک کردن سایت است...\n👛 ولت: `{WALLET}`")

if __name__ == "__main__":
    # ۱. روشن کردن سرور بیدارباش
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    print("--- PROGRAM STARTED ---")
    time.sleep(5)
    
    # ۲. تست فوری تلگرام
    send_telegram("🚀 سلام! اگر این پیام را می‌بینید یعنی اتصال برقرار است.")
    
    while True:
        check_airdrops()
        time.sleep(3600)
