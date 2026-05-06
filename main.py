import requests
import time
import os
import logging
from threading import Thread
from flask import Flask

# --- پیکربندی امنیتی و حذف کامل لاگ‌های مزاحم ---
logging.basicConfig(level=logging.CRITICAL)
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

class AirdropBot:
    def __init__(self):
        self.token = "8794852622:AAH9p2HSno2YPPIssRE5En0Ii2Wv84E8_pA"
        self.chat_id = "391754544"
        self.is_running = False
        self.scanned_count = 0
        self.found_airdrops = []
        self.session = requests.Session() # استفاده از Session برای سرعت بالاتر و مصرف کمتر
        self.last_update_id = 0

    def send_msg(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            self.session.post(url, data={'chat_id': self.chat_id, 'text': text, 'parse_mode': 'Markdown'}, timeout=10)
        except:
            pass

    def fetch_airdrop_data(self):
        """
        در این بخش ربات به منابع معتبر متصل می‌شود.
        به عنوان نمونه از یک API عمومی اخبار کریپتو/ایردراپ استفاده شده است.
        """
        try:
            # مثال: دریافت اطلاعات از یک منبع فرضی یا واقعی
            # شما می‌توانید API اختصاصی خود را اینجا جایگزین کنید
            response = self.session.get("https://api.coingecko.com/api/v3/news", timeout=15)
            if response.status_code == 200:
                return response.json()
        except:
            return None
        return None

    def monitor_engine(self):
        """هسته پردازشگر بی‌صدا"""
        while True:
            if self.is_running:
                data = self.fetch_airdrop_data()
                if data:
                    # منطق فیلتر کردن خبرهای مربوط به ایردراپ
                    # در اینجا ربات کلمات کلیدی را در اخبار جستجو می‌کند
                    for news in data.get('data', [])[:5]:
                        title = news.get('title', '')
                        if "airdrop" in title.lower() and title not in self.found_airdrops:
                            self.found_airdrops.append(title)
                            msg = f"🎁 **فرصت ایردراپ جدید شناسایی شد!**\n\n🔹 {title}\n\n🔗 [منبع خبر]({news.get('url')})"
                            self.send_msg(msg)
                
                self.scanned_count += 1
                if len(self.found_airdrops) > 50: self.found_airdrops.pop(0) # جلوگیری از پر شدن حافظه
                time.sleep(300) # هر 5 دقیقه یکبار چک می‌کند تا بن نشود
            else:
                time.sleep(10)

    def telegram_controller(self):
        """مدیریت دستورات با ساختار Long Polling بهینه"""
        while True:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getUpdates?offset={self.last_update_id + 1}&timeout=30"
                updates = self.session.get(url, timeout=35).json()
                
                for update in updates.get('result', []):
                    self.last_update_id = update['update_id']
                    if 'message' in update:
                        msg = update['message']
                        text = msg.get('text', '')
                        user_id = str(msg.get('chat', {}).get('id', ''))

                        if user_id == self.chat_id:
                            if text == "/start":
                                self.is_running = True
                                self.send_msg("🛰 **سیستم پایش ایردراپ فعال شد.**\nوضعیت: عملیاتی (Silent Mode)")
                            elif text == "/stop":
                                self.is_running = False
                                self.send_msg("🛑 **سیستم متوقف شد.**")
                            elif text == "/status":
                                status = "فعال ✅" if self.is_running else "متوقف 🛑"
                                self.send_msg(f"📊 **گزارش وضعیت:**\nوضعیت: {status}\nتعداد پایش: {self.scanned_count}")
            except:
                time.sleep(15)

# --- راه‌اندازی سرور Flask برای Cron-job و Render ---
bot = AirdropBot()
app = Flask(__name__)

@app.route('/')
def health_check():
    # خروجی بسیار کوتاه برای جلوگیری از لاگ حجیم
    return "OK", 200

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    # اجرای رشته‌های عملیاتی به صورت جداگانه
    Thread(target=bot.monitor_engine, daemon=True).start()
    Thread(target=bot.telegram_controller, daemon=True).start()
    
    # اجرای وب‌سرور
    run_web_server()
