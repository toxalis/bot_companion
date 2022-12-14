import re
import os
import json

import requests
# from bs4 import BeautifulSoup as BS
import dotenv

def parse_text(text):
    # r обозначает roar - сырая строка, чтобы символы \/ не интерпретировались
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    print(crypto)

with open ('answer.json') as f:
    dict = json.load(f)
    new_dict = {}
    for i in range(0,len(dict['data']['coins'])):
        name = dict['data']['coins'][i]['name']
        price = dict['data']['coins'][i]['quote']['USD']['price']
        new_dict.update({name: round(price,2)})

print(list(new_dict.items()))
print(new_dict)
print(len(dict['data']['coins']))

# parse_text('сколько стоит /eth?')