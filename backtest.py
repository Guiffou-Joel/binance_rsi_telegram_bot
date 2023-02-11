import datetime
from binance.client import Client
import pandas as pd
import numpy as np
import talib as ta

import datetime

import time


# definissez votre API key aet secret
API_KEY = ""
API_SECRET = ""
client = Client (API_KEY, API_SECRET, testnet=True)


coin = "BTCUSDT"
quantity = 100
increment = 0
time_frame = 5
rsi_periode = 14
sell_at = 70
buy_at = 30
running = False
last_command = False
current_price = False
last_price = False
last_order = False  ## buy sell
nb_buy = 0
last_quantity = 0

gain = 0
current_rsi = False

def buy_coin(price):
    global last_quantity
    global last_order
    q = quantity / price
    q = float(round(q, 5))
    print("Try to buy {} for {}$ = {} BTCBUSD".format(coin, quantity + (nb_buy * increment), q))
    try:
        # client.order_market_buy(symbol=coin, quantity=q)
        last_order = "Buy"
        last_quantity = q
    except Exception as e:
        print("Impossible to Buy {} at {} for {}$ = {}".format(coin, price, quantity, q))
        print(e)

def sell_coin(price):
    global last_order
    global gain
    #q = quantity / price
    q = last_quantity
    q = float(round(q, 5))
    print("Try to sell {} for {} BTCBUSD = {}$".format(coin, q, q * price))
    # try:
        # client.order_market_sell(symbol=coin, quantity=q)
    last_order = "Sell"
    gain = gain + ((q * price) - (quantity))
    print("Gain de {}".format(((q * price) - (quantity + (nb_buy * increment)))))
    # except Exception as e:
    #     print("Impossible to Sell {} at {} for {}$ = {}".format(coin, price, q * price, q))

# Récupération des données nécessaires
def get_coin_data(coin, tf, p):
    start = datetime.datetime(2022, 9, 1)
    try:
        data = client.get_historical_klines(coin, str(tf)+"m", "2021-12-31", )
        frame = pd.DataFrame(data)
        frame = frame.iloc[:, :5]
        frame.columns = ["Time", "Open", "High", "Low", "Close"]
        frame = frame.set_index("Time")
        frame.index = pd.to_datetime(frame.index, unit = "ms")
        frame = frame.astype(float)
        print(frame)
        return frame
    except Exception as e:
        print("Impossible de recevoir les données")
        print(e)
        print("\nLe programme continue tout de mm de fonctionner")
        return pd.DataFrame()

# Calcul du RSI
def rsi_calculation(df):
    try:
        df["rsi"] = ta.RSI(np.array(df["Close"]), timeperiod = rsi_periode)
        df.dropna(inplace = True)
        print(df)
        return df
    except Exception as e:
        print("Erreur lors du calcul du RSI")
        print(e)
        print("\nLe programme continue tout de mm de fonctionner")
        return pd.DataFrame()

def main():
    df = rsi_calculation(get_coin_data(coin, time_frame, rsi_periode))
    for i in df.index:
        rsi = df["rsi"][i]
        price = df["Close"][i]
        if rsi <= buy_at and (not last_order == "Buy"):
            buy_coin(price)
        elif(rsi >= sell_at and (last_order == "Buy")):
            sell_coin(price)
    
    print("Le gain est de: {}$".format(gain))
        

if __name__ == "__main__":
    main()