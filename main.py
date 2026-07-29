import telebot
import requests

BOT_TOKEN = "8856669884:AAHOyZs7AOySBE1myPPDaiiCVnxVnRo6Um8"
DIFY_API_KEY = "app-BSbTevNCtZkKQhdEqtMO0emQ"
DIFY_API_URL = "https://dify.ai"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    tz_text = message.text
    status_msg = bot.reply_to(message, "⏳ TZ qabul qilindi. SMM post va rasm tayyorlanmoqda, iltimos kuting...")

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": {},
        "query": tz_text,
        "response_mode": "blocking",
        "user": str(message.from_user.id)
    }

    try:
        response = requests.post(DIFY_API_URL, json=data, headers=headers).json()
        tayyor_javob = response.get('answer', 'Xatolik: Dify-dan bo\'sh javob qaytdi.')
        bot.send_message(message.chat.id, tayyor_javob)
        bot.delete_message(message.chat.id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik yuz berdi: {str(e)}", message.chat.id, status_msg.message_id)

import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

