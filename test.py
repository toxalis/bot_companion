import requests
# from bs4 import BeautifulSoup as BS
import os
import dotenv

# Команда dotenv.find_dotenv() находит файл .env    Вместо нее можно написать dotenv.load_dotenv('.env'
dotenv.load_dotenv(dotenv.find_dotenv())

print(os.getenv('bot'))

