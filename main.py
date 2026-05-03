import requests
from bs4 import BeautifulSoup
import time
import os
from threading import Thread
from flask import Flask

# اطلاعات شما که مستقیم در کد قرار داده شد
TELEGRAM_TOKEN = '8740696167:AAHSCQete8X7EMDVcFovV9RBjaJnMy-KEJA'
CHAT_ID = '391754544'

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and searching for Airdrops..."

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

seen_airdrops = set()

def check_for_airdrops():
    print("Checking for new airdrops...")
    url = "https://airdrops.io/latest/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        airdrops = soup.find_all('article', class_='air-article')
        
        for air in airdrops:
            try:
                name = air.find('div', class_='air-content').find('a').text.strip()
                link = air.find('div', class_='air-content').find('a')['href']
                
                if name not in seen_airdrops:
                    msg = f"🚀 **ایردراپ جدید پیدا شد!**\n\n📌 نام پروژه: `{name}`\n🔗 لینک بررسی: {link}\n\n✅ همین حالا اقدام کنید!"
                    send_telegram(msg)
                    seen_airdrops.add(name)
                    print(f"New found: {name}")
            except:
                continue
    except Exception as e:
        print(f"Connection error: {e}")

def bot_loop():
    # ارسال پیام اولیه برای اطمینان از صحت کارکرد
    send_telegram("🤖 ربات جستجوگر شما با موفقیت روشن شد و در حال جستجو است...")
    while True:
        check_for_airdrops()
        # هر ۳۰ دقیقه یکبار چک می‌کند
        time.sleep(1800)

if __name__ == "__main__":
    # شروع تردِ جستجوگر
    t = Thread(target=bot_loop)
    t.start()
    
    # شروع سرور برای جلوگیری از خاموشی Render
    run_web_server()
