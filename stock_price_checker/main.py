import json
# import os
from datetime import datetime, timedelta

import requests

from environs import Env

env = Env()  # Создаем экземпляр класса Env
env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

API_KEY = env('FINNHUB_API_KEY')  # Получаем и сохраняем значение переменной окружения в переменную bot_token




# API_KEY = os.getenv('FINNHUB_API_KEY')

BASE_URL = 'https://finnhub.io/api/v1/'
DAYS_BACK = 7
SYMBOL = "MSFT"


def check_price():
    url = f"{BASE_URL}quote?symbol={SYMBOL}&token={API_KEY}"
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)

    params = {
        'symbol': SYMBOL,
        'resolution': 'D',
        'from': int(datetime.timestamp(datetime.now() - timedelta(days=DAYS_BACK))),
        'to': int(datetime.timestamp(datetime.now())),
        'token': API_KEY
    }
    url = f"{BASE_URL}stock/candle"
    response = requests.get(url, params=params)
    data_candles = json.loads(response.text)
    # last_days_back_average = sum(data_candles['c']) / len(data_candles['c'])

    if 'c' in data_candles and len(data_candles['c']) > 0:
        last_days_back_average = sum(data_candles['c']) / len(data_candles['c'])
        if data['c'] > last_days_back_average:
            print(f"Цена акции Apple выше средней цены за последние {DAYS_BACK} дней")
        else:
            print(f"Цена акции Apple ниже средней цены за последние {DAYS_BACK} дней")
    else:
        print(f"Невозможно получить данные о цене акции за последние {DAYS_BACK} дней")


if __name__ == '__main__':
    check_price()
