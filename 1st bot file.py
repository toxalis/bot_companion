#Изменение системных переменных среды
# бот для тестирования общения с человеком с применением нескольких функций

import os
import dotenv

import telebot
from telebot import types  # types - для создания кнопок
import requests
from bs4 import BeautifulSoup as BS

import game

# Команда dotenv.find_dotenv() находит файл .env    Вместо нее можно написать dotenv.load_dotenv('.env')
dotenv.load_dotenv(dotenv.find_dotenv())
# Находим ключ для переменной bot. Альтенативная запись bot = os.getenv('bot_token')
BOT_TOKEN = os.environ['BOT_TOKEN']

# Создаем переменную bot и вставляем в нее ключ нашего бота
bot = telebot.TeleBot(BOT_TOKEN) # https://t.me/Companion_1st_bot

# Отслеживание комманд пользователей
@bot.message_handler(commands=['start'])
# Создаем функцию (принимает сообщение от пользователя)
def start(message):
    # Получаем информацию  о пользователе
    if message.from_user.last_name is None:
        mess = f'Привет, <b>{message.from_user.first_name}</b>'
    else:
        mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'

    # Отправляем сообщение пользователю
    # в send_message первым параметром указывается чат, в который отпр сообщ.
    # Через сообщение получаем id чата и в него же отправляем сообщение
    # Вторым параметром само сообщение
    # Третим параметром - режима отправки (просто текст или html,
    # что позволяет отправлять теги
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['talk'])
def com2(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)
    rmk.add(types.KeyboardButton("Да"),types.KeyboardButton("Нет"))
    msg = bot.send_message(message.chat.id, "Желаете начать беседу?", reply_markup = rmk)
    # Указываем название переменной и функцию, в которую ее надо передать
    bot.register_next_step_handler(msg, user_answer)

def user_answer(message):
    #Обрабатываем ответ пользователя
    if message.text == 'Да':
        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)
        rmk.add(types.KeyboardButton("О погоде"), types.KeyboardButton("Хочу анекдот"), types.KeyboardButton("Начать новую беседу"))
        msg = bot.send_message(message.chat.id, "О чем хотите поговорить?", reply_markup=rmk)
        bot.register_next_step_handler(msg, about)
    elif message.text == 'Нет':
        rmk = types.ReplyKeyboardRemove(selective=False)  # Удаляем клавиатуру
        bot.send_message(message.chat.id, 'Значит в другой раз 👋', reply_markup=rmk)
    else:
        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)
        rmk.add(types.KeyboardButton("О погоде"), types.KeyboardButton("Хочу анекдот"), types.KeyboardButton("Выйти в меню"))
        msg = bot.send_message(message.chat.id, "Я тебя не понимаю 😕", reply_markup=rmk)
        bot.register_next_step_handler(msg, user_answer)
        # bot.send_message(message.chat.id, 'Я тебя не понимаю')

def about(message):
    if message.text == 'О погоде':
        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)
        rmk.add(types.KeyboardButton("О погоде"), types.KeyboardButton("Хочу анекдот"), types.KeyboardButton("Выйти в меню"))
        msg = bot.send_message(message.chat.id, "Погода ништяк", reply_markup=rmk)
        bot.register_next_step_handler(msg, about)

        # bot.send_message(message.chat.id, 'Погода ништяк')
    elif message.text == 'Хочу анекдот' or message.text == 'Хочу ещё анекдот':
        bot.send_chat_action(message.chat.id, 'typing') # Пока выпоняется запрос бот "...печатает"
        url = 'https://www.anekdot.ru/random/anekdot/'
        response = requests.get(url)
        soup = BS(response.content, 'lxml')
        joke = soup.find('div', class_='text').text.strip()

        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)
        rmk.add(types.KeyboardButton("О погоде"), types.KeyboardButton("Хочу ещё анекдот"), types.KeyboardButton("Выйти в меню"))
        msg = bot.send_message(message.chat.id, joke, reply_markup=rmk)
        bot.register_next_step_handler(msg, about)

        # bot.send_message(message.chat.id, 'Заходят два программиста в бар...')

    elif message.text == 'Выйти в меню':
        rmk = types.ReplyKeyboardRemove(selective=False)  # Удаляем клавиатуру
        bot.send_message(message.chat.id, 'Выберите команду из меню', reply_markup=rmk)
    else:
        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 2)
        rmk.add(types.KeyboardButton("О погоде"), types.KeyboardButton("Хочу анекдот"), types.KeyboardButton("Выйти в меню"))
        msg = bot.send_message(message.chat.id, "Я тебя не понимаю 😕", reply_markup=rmk)
        bot.register_next_step_handler(msg, about)


#Сохранение ответов пользователя (? уточнить зачем нужно и когда использовать)
# bot.enable_save_next_step_handlers(delay=2)
# bot.load_next_step_handlers()
# Запускаем бота на непрерывное выполнение
bot.polling(none_stop=True)
