import requests
import smtplib
import os
from dotenv import load_dotenv
from twilio.rest import Client

STOCK = 'TSLA'
COMPANY_NAME = 'Tesla Inc'

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

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
    news_parameters = {
        'apiKey': os.getenv("API_KEY_FOR_NEWS"),
        'qInTitle': COMPANY_NAME
    }
    response_for_news = requests.get('https://newsapi.org/v2/everything', params=news_parameters)
    response_for_news.raise_for_status()
    articles = response_for_news.json()['articles']
    three_articles = articles[0:3]
    print(three_articles)

    formatted_articles = [f"Headline: {article['title']}. \nBrief:{article['description']}" for article in
                          three_articles]
    # do smtp or twilio
    message = "Subject: About Stocks\n\n" + "\n\n".join(formatted_articles)
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(os.getenv("MY_EMAIL"), os.getenv("MY_PASSWORD"))
        connection.sendmail(from_addr=os.getenv("MY_EMAIL"), to_addrs=os.getenv("MY_EMAIL"), msg=message.encode("utf-8"))

    # twilio as sms
    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # for article in formatted_articles:
    #     message = client.messages.create(body = article, from_ = "+18445438763", to ="+15103207767")
