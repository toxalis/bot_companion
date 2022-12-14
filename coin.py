# Тестированиие webhook для получения информации через API сайта в боте. на сайте coinmarketcap поменяли API
# и бесплатно получать цены любой монеты уже нельзя (не нашел как). Делал по видосу:
# https://www.youtube.com/watch?v=Al7hkU6RO9M
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# <блок взятый с сайта>
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
parameters = {
  'id' : '605e2ce9d41eae1066535f7c',
  'start':'1',
  'limit':'100',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '7d44c90b-3f2b-4a20-bc1c-54cfd30bf473',
}

session = Session()
session.headers.update(headers)
# </блок взятый с сайта>

# Запись ответа от сервера в красивый json файл
# def write_json(data, filename='answer.json'):
#   with open(filename, 'w') as f:
#     json.dump(data, f, indent=2, ensure_ascii=False)


try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  # write_json(data) запись полученного с сайта словаря в файл
  new_dict = {}
  for i in range(0, len(data['data']['coins'])):
    name = data['data']['coins'][i]['name']
    price = data['data']['coins'][i]['quote']['USD']['price']
    new_dict.update({name: round(price, 2)})
  print(new_dict)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)