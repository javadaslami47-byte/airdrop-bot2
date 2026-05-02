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
    return "Bot is Active!"

def send_telegram(msg):
    # استفاده از متد GET برای پایداری بیشتر در سرورهای رایگان
    url = f"https://telegram.org{TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': msg,
        'parse_mode': 'Markdown'
    }
    try:
        res = requests.get(url, params=params, timeout=20)
        print(f"Telegram Status: {res.status_code}")
        return res.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_airdrops():
    url = "https://airdrops.io"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        # (بخش اسکرپینگ مشابه قبل)
        print("Checking for new airdrops...")
    except: pass

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    
    time.sleep(5)
    # تست فوری - اگر این نیامد، یعنی توکن یا چت‌آیدی ایراد دارد
    send_telegram("🚀 **تست نهایی:** اتصال برقرار شد!")
    
    while True:
        get_latest_airdrops()
        time.sleep(3600)
