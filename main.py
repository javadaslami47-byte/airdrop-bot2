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
FILE_NAME = "seen_airdrops.txt"

app = Flask('')

@app.route('/')
def home():
    return "<h1>Bot is Active!</h1>"

def send_telegram(msg):
    # آدرس دهی دقیق با استفاده از متغیر TOKEN
    # نکته: نباید کلمه 'bot' را از آدرس زیر حذف کنید
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': msg,
        'parse_mode': 'Markdown'
    }
    try:
        # استفاده از Timeout طولانی‌تر برای جلوگیری از خطای تونل
        res = requests.post(url, json=payload, timeout=30)
        print(f"Telegram Log: {res.status_code} - {res.text}")
        return res.status_code == 200
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

def get_latest_airdrops():
    url = "https://airdrops.io"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'w') as f: pass
        response = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(response.text, 'html.parser')
        airdrops = soup.find_all('article', class_='air-article')
        
        with open(FILE_NAME, 'r') as f:
            seen_items = f.read().splitlines()

        for air in airdrops:
            try:
                link_tag = air.find('div', class_='air-content').find('a')
                name = link_tag.text.strip()
                link = link_tag['href']
                if name not in seen_items:
                    msg = f"🚀 **ایردراپ جدید!**\n\n📌 پروژه: `{name}`\n👛 ولت: `{WALLET}`\n🔗 [لینک شرکت]({link})"
                    if send_telegram(msg):
                        with open(FILE_NAME, 'a') as f:
                            f.write(name + "\n")
            except: continue
    except Exception as scrap_err:
        print(f"Scraping failed: {scrap_err}")

def run():
    # تنظیم پورت برای رفع خطای Port Binding
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # ۱. بیدار نگه داشتن سرور
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    print("Program started...")
    time.sleep(10) # زمان برای پایداری پورت
    
    # ۲. تست فوری اتصال
    send_telegram("✅ **اتصال عمیق بررسی و اصلاح شد!** ربات اکنون فعال است.")
    
    while True:
        get_latest_airdrops()
        time.sleep(3600)
