import os
import requests
from datetime import date, timedelta
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

STOCK = 'TSLA'
COMPANY_NAME = os.getSTOCK = os.getenv('COMPANY_NAME')
API_KEY_ALPHAVANTAGE = os.getSTOCK = os.getenv('API_KEY_ALPHAVANTAGE')
API_KEY_NEWSAPI = os.getSTOCK = os.getenv('API_KEY_NEWSAPI')
today = date.today()

# TWILIO CONFIG:
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getACCOUNT_SID = os.getenv('AUTH_TOKEN')

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def get_stock_data():
    uri = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': STOCK,
        'apikey': API_KEY_ALPHAVANTAGE,
    }
    res = requests.get(uri,  params=params)
    res.raise_for_status()
    return res.json()


def get_news_data():
    uri = 'http://newsapi.org/v2/everything'
    params = {
        'q': 'tesla',
        'from': today.strftime(r'%Y-%m-%d'),
        'sortBy': 'publishedAt',
        'apiKey': API_KEY_NEWSAPI,
        'language': 'en',
        'pageSize': 1
    }
    res = requests.get(uri, params=params)
    res.raise_for_status()
    return res.json()


def send_message(body: str):
    message = client.messages.create(
        body=body,
        from_='+12013088331',
        to='+573005070482'
    )
    return message.sid


def make_message():
    day_of_week = today.weekday()
    if day_of_week == 6 or day_of_week == 5:
        return 'The market cap today isn\'t open 😣'
    stock_data = get_stock_data()
    dataa = stock_data['Time Series (Daily)'][today.strftime(r'%Y-%m-%d')]
    open_m = float(dataa['1. open'])
    close_m = float(dataa['4. close'])
    diff = close_m-open_m
    sign = None
    if diff >= 0:
        sign = f'{STOCK}: 🔺'
    else:
        sign = f'{STOCK}: 🔻'
    percentage = abs(round(100*close_m/open_m)-100)
    sign += str(percentage)+'%'
    article = get_news_data()
    headline = article['articles'][0]['title']
    brief = article['articles'][0]['description']
    message = f'''
    {sign}
    Headline: {headline}
    Brief: {brief}
    '''
    return message


if __name__ == '__main__':
    message = make_message()
    transaction_id = send_message(message)
    print(f'Message sended with id: {transaction_id}')
