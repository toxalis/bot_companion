#Тестирование webhook

import os
import json

import dotenv
import telebot
import requests
import flask


dotenv.load_dotenv(dotenv.find_dotenv())
BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN) # https://t.me/Companion_1st_bot

app = flask.Flask(__name__)

url = f'https://api.telegram.org/bot{BOT_TOKEN}/'
def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_message(chat_id, text='bla-bla-bla'):
    url_ = url + 'sendMessage'
    answer = {'chat_id': chat_id, 'text':text, 'parse_mode':'html'}
    r = requests.post(url_, json=answer)
    return r.json()

@app.route('/', methods=['POST','GET'])
def index():
    if flask.request.method == 'POST':
        r = flask.request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        if any(map(message.lower().__contains__,['прив', 'хай', 'hello', 'hi'])):
            mess = f"Привет, <b>{r['message']['chat']['first_name']}!</b>"
        else:
            mess = 'Я тебя не понимаю'
        send_message(chat_id, mess)

        # write_json(r)
        return flask.jsonify(r)
    return'<h1>Bot welcomes you</h1>'

if __name__ == '__main__':
    app.run()

# прописать в терминале: C:\PyCharm_Projects\ngrok http 5000
# скопировать url адрес страницы "Bot welcomes you" (https://6d63-93-170-228-226.eu.ngrok.io/)
# вставить в строку браузера для установки webhook
# print(f'{url}setWebhook?url=https://6d63-93-170-228-226.eu.ngrok.io/')




