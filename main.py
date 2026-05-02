import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask
from threading import Thread

# --- تنظیمات شما (دقیق چک شده) ---
TOKEN = '8740696167:AAHSCQete8X7EMDVcFovV9RBjaJnMy-KEJA'
CHAT_ID = '391754544'
WALLET = 'UQDo6vfO8kdvGNATer9nsTEki3ljoGLKoHmS2opGsafmSwxj'
FILE_NAME = "seen_airdrops.txt"

app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def send_telegram(msg):
    # آدرس اصلاح شده با ساختار استاندارد تلگرام
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': msg,
        'parse_mode': 'Markdown'
    }
    try:
        res = requests.post(url, json=payload, timeout=20)
        print(f"Telegram Log: {res.status_code}")
        return res.status_code == 200
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

def get_latest_airdrops():
    url = "https://airdrops.io"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'w') as f: pass
        response = requests.get(url, headers=headers, timeout=20)
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
                    msg = f"🚀 **ایردراپ جدید!**\n\n📌 پروژه: `{name}`\n👛 ولت: `{WALLET}`\n🔗 [لینک]({link})"
                    if send_telegram(msg):
                        with open(FILE_NAME, 'a') as f:
                            f.write(name + "\n")
            except: continue
    except: pass

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    print("برنامه در حال اجراست...")
    time.sleep(10)
    # تست اولیه
    send_telegram("✅ **اتصال اصلاح شد!** ربات اکنون به درستی به تلگرام متصل است.")
    
    while True:
        get_latest_airdrops()
        time.sleep(3600)
