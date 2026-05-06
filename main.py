import requests
import os
import time
import logging
from threading import Thread
from flask import Flask

# --- تنظیمات اختصاصی شما ---
TELEGRAM_TOKEN = '8794852622:AAH9p2HSno2YPPIssRE5En0Ii2Wv84E8_pA'
CHAT_ID = '391754544'

# --- تنظیمات سیستمی برای حذف کامل لاگ‌ها و جلوگیری از خطای Output too large ---
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

app = Flask('')

# وضعیت ربات
bot_status = {
    "active": False,
    "last_check": "Never",
    "alerts_sent": 0
}

@app.route('/')
def home():
    # صفحه اصلی برای تایید زنده بودن توسط Cron-job
    return f"Airdrop Bot is Running. Status: {bot_status['active']}"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, data=payload, timeout=15)
    except:
        pass

def airdrop_logic():
    """
    منطق اصلی ربات ایردراپ شما اینجا قرار می‌گیرد.
    مثلاً چک کردن سایت‌ها یا انجام تسک‌ها.
    """
    while True:
        if bot_status["active"]:
            try:
                # اینجا کدی که برای ایردراپ دارید را قرار دهید
                # برای مثال: چک کردن یک API برای ایردراپ جدید
                
                # به عنوان نمونه:
                # if found_new_airdrop:
                #    send_telegram("🎁 ایردراپ جدید پیدا شد!")
                #    bot_status["alerts_sent"] += 1
                
                bot_status["last_check"] = time.strftime("%H:%M:%S")
                
                # وقفه طولانی‌تر برای جلوگیری از فشار به سرور (مثلاً هر 5 دقیقه)
                time.sleep(300) 
            except:
                time.sleep(60)
        else:
            time.sleep(10)

def telegram_listener():
    """شنود دستورات شما در تلگرام"""
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}&timeout=20"
            res = requests.get(url, timeout=25).json()
            
            for update in res.get('result', []):
                offset = update['update_id'] + 1
                if 'message' in update:
                    text = update['message'].get('text', '')
                    user_id = str(update['message'].get('chat', {}).get('id', ''))
                    
                    if user_id == CHAT_ID:
                        if text == "/start":
                            bot_status["active"] = True
                            send_telegram("🚀 **ربات ایردراپ فعال شد.**\nسیستم به صورت بی‌صدا در حال بررسی است.")
                        
                        elif text == "/stop":
                            bot_status["active"] = False
                            send_telegram("🛑 **ربات متوقف شد.**")
                            
                        elif text == "/status":
                            msg = (f"📊 **وضعیت ربات ایردراپ:**\n"
                                   f"وضعیت: {'فعال' if bot_status['active'] else 'غیرفعال'}\n"
                                   f"آخرین بررسی: {bot_status['last_check']}\n"
                                   f"تعداد اعلان‌ها: {bot_status['alerts_sent']}")
                            send_telegram(msg)
        except:
            time.sleep(10)
        time.sleep(1)

if __name__ == "__main__":
    # اجرای بخش‌های مختلف در پس‌زمینه بدون تولید لاگ در کنسول
    Thread(target=airdrop_logic, daemon=True).start()
    Thread(target=telegram_listener, daemon=True).start()
    
    # اجرای وب‌سرور برای Cron-job و Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
