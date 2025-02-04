import requests
import smtplib
import os
from dotenv import load_dotenv

STOCK = 'TSLA'
COMPANY_NAME = 'Tesla Inc'

load_dotenv()

parameters = {
    'function' :'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': os.getenv("API_KEY_FOR_STOCK_ENDPOINT")
}

response = requests.get('https://www.alphavantage.co/query', params=parameters)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)

if abs(diff_percent) > 1:
    pass