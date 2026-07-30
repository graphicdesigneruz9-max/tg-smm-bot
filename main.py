import os
import telebot
import requests
from flask import Flask, request

# KALITLARNI SHU YERGA YOZING
BOT_TOKEN = "8856669884:AAHOyZs7AOySBE1myPPDaiiCVnxVnRo6Um8"
DIFY_API_KEY = "app-RkqVjCJsB7Xhg6uHVREp91JQ"

# Yevropa serveri uchun aniq API manzili
DIFY_API_URL = "https://dify.ai"
RENDER_URL = "https://onrender.com"

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Bot is live!"

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
        response = requests.post(DIFY_API_URL, json=data, headers=headers)
        res_json = response.json()
        
        tayyor_javob = res_json.get('answer', '')
        if not tayyor_javob and 'data' in res_json:
            tayyor_javob = res_json['data'].get('outputs', {}).get('text', '')
            
        if not tayyor_javob:
            tayyor_javob = "Dify tizimidan matn qabul qilinmadi. Bloklarni tekshiring."

        bot.send_message(message.chat.id, tayyor_javob)
        bot.delete_message(message.chat.id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik: {str(e)}", message.chat.id, status_msg.message_id)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
