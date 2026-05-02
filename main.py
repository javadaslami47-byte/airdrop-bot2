import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask
from threading import Thread

# --- تنظیمات اختصاصی شما ---
TELEGRAM_TOKEN = '8740696167:AAHSCQete8X7EMDVcFovV9RBjaJnMy-KEJA'
CHAT_ID = '391754544'
MY_WALLET = 'UQDo6vfO8kdvGNATer9nsTEki3ljoGLKoHmS2opGsafmSwxj'
FILE_NAME = "seen_airdrops.txt"

# --- بخش وب‌سرور برای زنده نگه داشتن در Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- بخش اصلی ربات ---
def send_telegram(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, json=payload, timeout=20)
    except:
        pass

def get_latest_airdrops():
    url = "https://airdrops.io"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'w') as f: pass
        
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        airdrops = soup.find_all('article', class_='air-article')
        
        with open(FILE_NAME, 'r') as f:
            seen_items = f.read().splitlines()

        for air in airdrops:
            try:
                content = air.find('div', class_='air-content').find('a')
                name = content.text.strip()
                link = content['href']
                if name not in seen_items:
                    msg = f"🚀 **ایردراپ جدید!**\n\n📌 پروژه: `{name}`\n👛 ولت: `{MY_WALLET}`\n🔗 [لینک]({link})"
                    send_telegram(msg)
                    with open(FILE_NAME, 'a') as f:
                        f.write(name + "\n")
            except: continue
    except:
        pass

if __name__ == "__main__":
    print("Bot is starting...")
    keep_alive() # فعال کردن وب‌سرور
    send_telegram("✅ ربات ایردراپ در Render با موفقیت فعال شد!")
    
    while True:
        get_latest_airdrops()
        time.sleep(3600) # بررسی هر ۱ ساعت
