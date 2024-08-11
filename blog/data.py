from cmath import rect
import requests
import json
from newsapi import NewsApiClient
import pycountry
from pya3 import *
# import talib as ta
from time import sleep
import datetime
import sqlite3



def fetchCompanyData(cmpName):
    f = open('StockCode.json')
    data=json.load(f)
    url = (f'''https://newsapi.org/v2/everything?q={data[cmpName]}&from=2023-04-05&sortBy=popularity&apiKey=07b2c6a4274c43a399ad60bf453b81fe''')
    response = requests.get(url)
    if len(response.json()['articles'])==0:
        return f"No News available for {cmpName}"

    return response.json()['articles']


def RecentNews():
    newsapi = NewsApiClient(api_key='07b2c6a4274c43a399ad60bf453b81fe')
    input_country ="India"
    input_countries = [f'{input_country.strip()}']
    countries = {}

    for country in pycountry.countries:
        countries[country.name] = country.alpha_2

    codes = [countries.get(country.title(), 'Unknown code')
            for country in input_countries]

    top_headlines = newsapi.get_top_headlines(category=f'{"Business".lower()}', language='en', country=f'{codes[0].lower()}')
    Headlines = top_headlines['articles']
    news=[]
    if Headlines:
            for articles in Headlines:
                b = articles['title'][::-1].index("-")
                if "news" in (articles['title'][-b+1:]).lower():
                    news.append(f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.")
                else:
                    news.append(f"{articles['title'][-b+1:]} News: {articles['title'][:-b-2]}.")
    return news 






# Required Details
api_key = "Zq4pSklHqS9BJptGOPFH87ZQH2Ql8bDo6Dnbpyl55MXnvBO9nWQ7ClxWHaluviuXiOGNAlRR0ZpK2d9PJzRaIkyBakSJ61osnNWUmsDz6VFOHOB9nlPG9eknG5KCOcrd"         # Get from https://a3.aliceblueonline.com      After Login go to "Apps" section and create API
user_id = "AB032684"
count=0

def calling(cmpname,quantity,Id):
    global alice, userid, apikey, count
    EMA_CROSS_SCRIP = f"{cmpname}-EQ"
    alice = Aliceblue(user_id=user_id, api_key=api_key)
    print(alice.get_session_id())  
    alice.get_contract_master("NSE")
    alice.get_contract_master("BSE")
    alice.get_contract_master("INDICES")
    ins_scrip = alice.get_instrument_by_symbol('NSE', EMA_CROSS_SCRIP)
    if Id==1: 
        buy_signal(ins_scrip,quantity)
    else:
        sell_signal(ins_scrip,quantity)    


def calculate_ema(prices, days, smoothing=2):
    ema = []
    for i in range(days):
        # ema.append(sum(prices[:days]) / days)
        ema.append(prices[0])
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


def EMA_algo(ins_scrip):
    from_datetime = datetime.datetime.now() - datetime.timedelta(days=60)        # From last & days
    to_datetime = datetime.datetime.now()       # To now
    interval = "D"          # ["1", "D"]
    df = alice.get_historical(ins_scrip, from_datetime, to_datetime, interval, indices=False)
    # print(df)

    # df["ema_5"] = calculate_ema(df["close"], 5)
    # df["ema_13"] = calculate_ema(df["close"], 13)
    df["ema_5"] = ta.EMA(df["close"], timeperiod=5)
    df["ema_13"] = ta.EMA(df["close"], timeperiod=13)
    # print(ema1, ema2)
    print(df)



def buy_signal(ins_scrip,quantity):
    print("Inside buy_signal function")
    print(alice.place_order(transaction_type=TransactionType.Buy,
                          instrument=ins_scrip,
                          quantity=quantity,
                          order_type=OrderType.Limit,
                          product_type=ProductType.Delivery,
                          price=1.0,
                          trigger_price=None,
                          stop_loss=None,
                          square_off=None,
                          trailing_sl=None,
                          is_amo=False,
                          order_tag='buy'))


def sell_signal(ins_scrip,quantity):
    print("Inside sell_signal function")
    print(alice.place_order(transaction_type=TransactionType.Sell,
                            instrument=ins_scrip,
                            quantity=quantity,
                            order_type=OrderType.Limit,
                            product_type=ProductType.Delivery,
                            price=5000.0,
                            trigger_price=None,
                            stop_loss=None,
                            square_off=None,
                            trailing_sl=None,
                            is_amo=False,
                            order_tag='sell'))
