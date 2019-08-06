import telebot
import os
from flask import Flask, request
from telebot.types import InlineQueryResultArticle
from telebot.types import InputTextMessageContent

API_TOKEN = os.getenv('TG_API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text=f'First Name:, {message.chat.first_name}')
    bot.send_message(chat_id=message.chat.id, text=f'Last Name:{message.chat.last_name}')
    bot.send_message(chat_id=message.chat.id, text=f'Id:, {message.chat.id}')


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    if message.forward_from is None:
        bot.send_message(chat_id=message.chat.id, text=f'First Name:, {message.chat.first_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Last Name:{message.chat.last_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Id:, {message.chat.id}')
    else:
        bot.send_message(chat_id=message.chat.id, text=f'First Name:, {message.forward_from.first_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Last Name:{message.forward_from.last_name}')
        bot.send_message(chat_id=message.chat.id, text=f'Id:, {message.forward_from.id}')

@bot.inline_handler(func=lambda query: 'алиас' in query.query)
def answer_alias_query(inline_query):
    username = inline_query.from_user.username
    alias_article = InlineQueryResultArticle(
        id='0',
        title='Отправить мой алиас',
        description='Отправить свой алиас в чат!',
        input_message_content=InputTextMessageContent(
            message_text=f'Мой алиас: @{username}'
        )
    )

    bot.answer_inline_query(
        switch_pm_text = '1',
        switch_pm_parameter = '1',
        inline_query_id=inline_query.id,
        results=[alias_article],
        cache_time=0
    )



@server.route('/' + API_TOKEN, methods=['POST'])
def get_message():
    json_update = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_update)

    bot.process_new_updates([update])
    return '', 200


bot.remove_webhook()
bot.set_webhook(url=os.getenv('WEBHOOK_URL') + API_TOKEN)
server.run(host="0.0.0.0", port=int(os.getenv('PORT', 8443)))
