import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = "8856669884:AAHOyZs7AOySBE1myPPDaiiCVnxVnRo6Um8"
DIFY_API_KEY = "app-RkqVjCJsB7Xhg6uHVREp91JQ"
DIFY_API_URL = "https://dify.ai"

# Render'da sizga berilgan asosiy havola (Oxirida slash '/' belgisiz yozing)
RENDER_URL = "https://onrender.com" 

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Bot is live and running!"

# Telegram xabarlarini qabul qiluvchi maxsus manzil
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    tz_text = message.text
    status_msg = bot.reply_to(message, "⏳ TZ qabul qilindi. SMM post tayyorlanmoqda, iltimos kuting...")
    
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

if __name__ == "__main__":
    # Telegram serverlariga webhook ulanishini o'rnatish
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
