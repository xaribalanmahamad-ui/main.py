import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = "8694548245:AAFr9eMAJtj-cnrHYzzIvvDGuVJzknNMA6k"
bot = telebot.TeleBot(TOKEN)
CHANNELS = ["@Channel1_kurdfile", "@Channel2_kurdferkary"]

def check_sub(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        except Exception:
            return False
    return True

def get_join_markup():
    markup = InlineKeyboardMarkup()
    for i, ch in enumerate(CHANNELS, 1):
        markup.add(InlineKeyboardButton(f"📢 Channel {i}", url=f"https://t.me/{ch.replace('@', '')}"))
    markup.add(InlineKeyboardButton("🔄 Check", callback_data="check_join"))
    return markup

def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📁 Files", callback_data="btn_files"),
        InlineKeyboardButton("🔑 Keys", callback_data="btn_keys")
    )
    markup.add(InlineKeyboardButton("📚 Tutorials", callback_data="btn_tutorial"))
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if check_sub(message.from_user.id):
        bot.send_message(message.chat.id, "Welcome! Select an option from the menu:", reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, "You must join all required channels first:", reply_markup=get_join_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    
    if call.data == "check_join":
        if check_sub(user_id):
            bot.answer_callback_query(call.id, "✅ Subscription verified!")
            bot.edit_message_text("Welcome! Select an option from the menu:", call.message.chat.id, call.message.message_id, reply_markup=get_main_menu())
        else:
            bot.answer_callback_query(call.id, "❌ You have not joined all channels yet!", show_alert=True)
            
    elif call.data == "btn_files":
        bot.send_message(call.message.chat.id, "📁 Files Section")
        
    elif call.data == "btn_keys":
        bot.send_message(call.message.chat.id, "🔑 Keys Section")
        
    elif call.data == "btn_tutorial":
        bot.send_message(call.message.chat.id, "📚 Tutorials Section")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    