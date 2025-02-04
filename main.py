import requests
import smtplib

STOCK = 'TSLA'
COMPANY_NAME = 'Tesla Inc'

parameters = {
    'function' :'TIME_SERIES_DAILY',
    'symbol': STOCK,
}
response = requests.get('https://www.alphavantage.co/query', params=parameters)