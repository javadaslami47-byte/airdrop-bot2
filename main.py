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

# --- تنظیمات وب‌سرور برای رفع خطای پورت در Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    # Render به این بخش برای تایید وضعیت Live نیاز دارد
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- توابع اصلی ربات ---
def send_telegram(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False
    }
    try:
        # ارسال درخواست با Timeout مناسب برای جلوگیری از فریز شدن
        response = requests.post(url, json=payload, timeout=20)
        print(f"Telegram Log: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return False

def get_latest_airdrops():
    url = "https://airdrops.io"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'w') as f: pass

        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200: return

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
                    msg = (f"🚀 **ایردراپ جدید یافت شد!**\n\n"
                           f"📌 پروژه: `{name}`\n"
                           f"👛 ولت: `{MY_WALLET}`\n"
                           f"🔗 [ورود به سایت]({link})")
                    
                    if send_telegram(msg):
                        with open(FILE_NAME, 'a') as f:
                            f.write(name + "\n")
            except:
                continue
    except Exception as e:
        print(f"Scraping Error: {e}")

if __name__ == "__main__":
    # ۱. روشن کردن وب‌سرور برای جلوگیری از ارور Port Binding
    keep_alive()
    
    # ۲. کمی صبر برای بالا آمدن سیستم
    time.sleep(10)
    
    print("Bot starting...")
    send_telegram("✅ **ربات با موفقیت در Render اصلاح و فعال شد!**")
    
    # ۳. حلقه اصلی بررسی
    while True:
        get_latest_airdrops()
        # بررسی هر ۱ ساعت
        time.sleep(3600)
