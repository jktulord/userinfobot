import telebot
from db import set_state, get_state
import os
from flask import Flask, request

API_TOKEN = os.getenv('TG_API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text=f'First Name:, {message.chat.first_name}')
    bot.send_message(chat_id=message.chat.id, text=f'Last Name:{message.chat.last_name}')
    bot.send_message(chat_id=message.chat.id, text=f'Id:, {message.chat.id}')

@bot.message_handler(func=lambda message: true)
def send_welcome(message):
    if message.forward_from == none:
        bot.send_message(chat_id=message.chat.id, text=f'First Name:, {message.chat.first_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Last Name:{message.chat.last_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Id:, {message.chat.id}')
    else:
        bot.send_message(chat_id=message.chat.id, text=f'First Name:, {message.forward_from.first_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Last Name:{message.forward_from.last_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Id:, {message.forward_from.id}')

@server.route('/' + API_TOKEN, methods=['POST'])
    def get_message():
        json_update = request.stream.read().decode('utf-8')
        update = telebot.types.Update.de_json(json_update)

        bot.process_new_updates([update])
        return '', 200

bot.remove_webhook()
bot.set_webhook(url=os.getenv('K') + API_TOKEN)
server.run(host="0.0.0.0", port=int(os.getenv('PORT', 8443)))
