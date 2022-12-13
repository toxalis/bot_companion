#Тестирование webhook

import os
import dotenv

import telebot
from telebot import types  # types - для создания кнопок
import requests
from bs4 import BeautifulSoup as BS

dotenv.load_dotenv(dotenv.find_dotenv())
BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN) # https://t.me/Companion_1st_bot

@bot.message_handler(content_types=['text'])
# Создаем функцию (принимает сообщение от пользователя)
def get_user_text(message):
    if message.text.lower().__contains__('привет'):
        mess = f'Привет, <b>{message.from_user.first_name}!</b>'
    else:
        mess = 'Я тебя не понимаю'
    bot.send_message(message.chat.id, mess, parse_mode='html')

bot.polling(none_stop=True)