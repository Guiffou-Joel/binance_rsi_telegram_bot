# api key uG0bj7aBZtgRLj4fm7aL0b3ssEJIB6AirSSQw6spvQpXv1LWSsMWTftrfHR0NmhO

# secret key usLZTFNVBbOTQV6oBAAngj7eoH44rNQod14NqE5ful7c0dhb2jWMdziKEw1sW5mH

# binance future api key 8796533e87e967c8cedc2e94d9c9f6f856164d0b7020f839cf31ae536ad9bc72
# binance future secret key 18ac60bbeb307fa55a1ec65a69a327a1d26e810dc19ad0a74e7c9a8f0fc6466b


# import the Binance client from python-binance module
#from tkinter import E
from glob import glob
from binance.client import Client

# import the telegram library
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# import the threading library
import threading

import datetime

import pandas as pd
import numpy as np
import talib as ta

# define your API key and secret
API_KEY = ""
API_SECRET = ""

# define telegram bot token
TOKEN = '5519961221:AAHakZZHjPwFjziT4CKl9xZJ1wsRQ_Js4to'

# define the client
client = Client (API_KEY, API_SECRET, testnet=True)

# CONFIG VARIABLES DEFINED HERE
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
    q = (quantity + (nb_buy * increment)) / price
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
    #q = quantity / price
    q = last_quantity
    q = float(round(q, 5))
    print("Try to sell {} for {} BTCBUSD = {}$".format(coin, q, q * price))
    try:
        # client.order_market_sell(symbol=coin, quantity=q)
        last_order = "Sell"
        gain = gain + ((q * price) - (quantity + (nb_buy * increment)))
        print("Gain de {}".format(((q * price) - (quantity + (nb_buy * increment)))))
    except Exception as e:
        print("Impossible to Sell {} at {} for {}$ = {}".format(coin, price, q * price, q))

def get_coin_price():
    try:
        r = client.get_symbol_ticker(symbol=coin)
        return float(r["price"])
    except Exception as e:
        print("Impossible de récupérer le prix du bitcoin depuis le serveur binance. Retentative.....")
        print(e)
        return False;

def run(update, context):
    global last_command
    global running
    if(running):
        update.message.reply_text('Votre robot binance est déjà en cours d\'exécution')
    else:
        if (quantity and sell_at and buy_at): # and not (API_KEY == "") and not (API_SECRET == "")):
            running = True
            update.message.reply_text('Votre robot binance a été lancé avec succes')
            print("Mis en marche du robot binance.......")
        else:
            update.message.reply_text('Vous devez définir tout les paramètres avant de démarer le bot binance')
    last_command = False

def stop(update, context):
    global running
    global last_command
    global current_price
    global nb_buy
    global quantity
    if(not running):
        update.message.reply_text('Votre robot binance est déjà a l\'arret')
    else:
        running = False
        update.message.reply_text('Votre robot binance a été arrété avec succes')
        print("Mise a l'arret du robot binance......")
    current_price = False
    last_command = False
    nb_buy = 0

def set_quantity(update, context):
    global last_command
    update.message.reply_text('Entrez la quantité de btc (en BUSD) a acheter et a vendre au format xxx.xxx')
    last_command = "Quantity"

def set_increment(update, context):
    global last_command
    update.message.reply_text('Entrez la quantité de btc (en BUSD) a ajouter après chaque achat au format xxx.xxx')
    last_command = "Increment"

def set_where_to_buy(update, context):
    global last_command
    update.message.reply_text('Entrez le prix au format xxx.xxx')
    last_command = "Buy"

def set_where_to_sell(update, context):
    global last_command
    update.message.reply_text('Entrez le prix au format xxx.xxx')
    last_command = "Sell"

def set_crypto(update, context):
    global last_command
    update.message.reply_text('Entrez le nom de la crypto au bon format. exemple: BTCUSDT')
    last_command = "Crypto"

def set_time_frame(update, context):
    global last_command
    update.message.reply_text('Entrez le time frame en nombre entier de minutes')
    last_command = "TF"

def set_rsi_periode(update, context):
    global last_command
    update.message.reply_text('Entrez la période du RSI en nombre entier')
    last_command = "RP"

# def set_api_key(update, context):
#     global last_command
#     update.message.reply_text('Entrez l\'api key binance')
#     last_command = "Api"

# def set_secret_key(update, context):
#     global last_command
#     update.message.reply_text('Entrez la secret key binance')
#     last_command = "Secret"

def status(update, context):
    global last_command
    update.message.reply_text("""
Bienvenue sur Binance BTC bot.

Achetez et vendez automatiquement le bitcoin sur binance a des prix précis !
Et ne manquez plus des opportunités

Voici les infos de votre robot binance :
- Etat : {}
- Niveau de vente : {}
- Niveau d'achet : {}
- Quantité initiale : {}$ 
- Incrementation : {}
- Api key binance : {}
- Secret key binance : {}
- Nombre Ordre d'achat éffectué : {}
- Ordre en cours : {}
- Time frame : {}
- Période du RSI : {}
- Gain : {}$
- RSI: {}
    """.format(running, sell_at, buy_at, quantity, increment, API_KEY, API_SECRET, nb_buy, last_order, time_frame, rsi_periode, gain, current_rsi))
    last_command = False

def hello(update, context):
    global last_command
    update.message.reply_text("Hello !\n Vous vous portez bien j'espère")
    last_command = False

def message(update, context):
    global last_command
    global buy_at
    global sell_at
    global API_KEY
    global API_SECRET
    global client
    global quantity
    global nb_buy
    global increment
    global time_frame
    global rsi_periode
    global coin
    if(last_command):
        if(last_command == "Crypto"):
            try:
                coin = update.message.text
                update.message.reply_text('Valeur enregistré avec success')
                last_command = False
            except:
                update.message.reply_text('Valeur incorrect, veillez reessayer')
        elif(last_command == "TF"):
            try:
                time_frame = int(update.message.text)
                update.message.reply_text('Valeur enregistré avec success')
                last_command = False
            except:
                update.message.reply_text('Valeur incorrect, veillez reessayer')
        elif(last_command == "RP"):
            try:
                rsi_periode = int(update.message.text)
                update.message.reply_text('Valeur enregistré avec success')
                last_command = False
            except:
                update.message.reply_text('Valeur incorrect, veillez reessayer')
        elif (last_command == "Increment"):
            try:
                increment = float(update.message.text)
                update.message.reply_text('Valeur enregistré avec success')
                last_command = False
            except:
                update.message.reply_text('Valeur incorrect, veillez reessayer')
        elif(last_command == "Buy"):
            try:
                buy_at = float(update.message.text)
                update.message.reply_text('Valeur enregistré avec success')
                last_command = False
            except:
                update.message.reply_text('Valeur incorrect, veillez reessayer')
        elif(last_command == "Sell"):
            try:
                sell_at = float(update.message.text)
                update.message.reply_text('Valeur enregistré avec success')
                last_command = False
            except:
                update.message.reply_text('Valeur incorrect, veillez reessayer')
        # elif(last_command == "Api"):
        #     try:
        #         API_KEY = update.message.text
        #         client = Client (API_KEY, API_SECRET, testnet=True)
        #         update.message.reply_text('Valeur enregistré avec success')
        #         last_command = False
        #     except:
        #         update.message.reply_text('Valeur incorrect, veillez reessayer')
        # elif(last_command == "Secret"):
        #     try:
        #         API_SECRET = update.message.text
        #         client = Client (API_KEY, API_SECRET, testnet=True)
        #         update.message.reply_text('Valeur enregistré avec success')
        #         last_command = False
        #     except:
        #         update.message.reply_text('Valeur incorrect, veillez reessayer')
        elif(last_command == "Quantity"):
            try:
                quantity = float(update.message.text)
                update.message.reply_text('Valeur enregistré avec success')
                last_command = False
                nb_buy = 0
            except:
                update.message.reply_text('Valeur incorrect, veillez reessayer')
        else:
            update.message.reply_text('un problème est survenue')
            print(last_command)
            last_command = False
    else:
        update.message.reply_text('Ce message est inconnue: ' + update.message.text)
        last_command = False

def start(update, context):
    update.message.reply_text("""
Bienvenue sur Binance BTC bot.

Achetez et vendez automatiquement le bitcoin sur binance a des prix précis !
Et ne manquez plus des opportunités

Les commandes disponibles sont :
- /run Pour Démarer le robot binance
- /set_crypto Pour définir la crypto a acheter et a vendre
- /set_time_frame Pour définir le time frame
- /set_rsi_periode Pour définir le nombre de période pour le calcul du rsi
- /stop Pour arréter le bot binance
- /status Pour afficher l'état et les infos du robot binance
- /set_where_to_buy Pour définir le niveau du rsi auquel acheter
- /set_where_to_sell Pour définir le niveau du rsi auquel vendre
- /set_quantity Pour définir la quatité de crypto a acheter et a vendre en dollar
- /set_increment Pour définir la quantité a ajouter après chaque achat
- /hello Pour saluer le bot !
    """)

# Récupération des données nécessaires
def get_coin_data(coin, tf, p):
    try:
        data = client.get_historical_klines(coin, str(tf)+"m", str(tf * (p * 2))+"min ago UTC")
        frame = pd.DataFrame(data)
        frame = frame.iloc[:, :5]
        frame.columns = ["Time", "Open", "High", "Low", "Close"]
        frame = frame.set_index("Time")
        frame.index = pd.to_datetime(frame.index, unit = "ms")
        frame = frame.astype(float)
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
        return df
    except Exception as e:
        print("Erreur lors du calcul du RSI")
        print(e)
        print("\nLe programme continue tout de mm de fonctionner")
        return pd.DataFrame()

# Mise en place de la stratégie basée sur le rsi
def main(name):
    global current_price
    global last_price
    global nb_buy
    global last_order
    global last_quantity
    global increment
    global current_rsi
    print("main : " + name)
    while True:
        if(running):
            #print("running")
            df = get_coin_data(coin, time_frame, rsi_periode)
            if(df.empty):
                continue
            df = rsi_calculation(df)
            if(df.empty):
                continue
            rsi = df.rsi.iloc[-1]
            print(f'Current close price is: ' + str(df.Close.iloc[-1]) + f' Current RSi value is: ' + str(rsi))
            current_rsi = rsi
            if rsi <= buy_at and (not last_order == "Buy"):
                price = get_coin_price(coin)
                if (price == False):
                    continue
                buy_coin(price)
            elif(rsi >= sell_at and (last_order == "Buy")):
                price = get_coin_price(coin)
                if (price == False):
                    continue
                sell_coin(price)
        else:
            #print("Not Running")
            pass

if __name__ == "__main__":
    print("running program...")

    now = datetime.datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Date et Heure =", dt_string)
    ts = now.timestamp()
    now = datetime.date.fromtimestamp(ts)

    expire_date = datetime.date(2022, 8, 9)
    #if (now > expire_date):
        #print("Cette version d'essaie a expiré. Veillez vous rapprocher du développeur GUIFFOU JOEL sur 5euros.com : https://5euros.com/profil/guiffou-joel")
        ## dd/mm/YY H:M:S
        #dt_string = expire_date.strftime("%d/%m/%Y")
        #print("Date d'expiration = ", dt_string)
        #exit()

    threading.Thread(target=main,args=(__name__,)).start()
    # La classe Updater permet de lire en continu ce qu'il se passe sur le channel
    updater = Updater(TOKEN, use_context=True)

    # Pour avoir accès au dispatcher plus facilement
    dp = updater.dispatcher

    # On ajoute des gestionnaires de commandes
    # On donne a CommandHandler la commande textuelle et une fonction associée
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("run", run))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("set_where_to_buy", set_where_to_buy))
    dp.add_handler(CommandHandler("set_where_to_sell", set_where_to_sell))
    dp.add_handler(CommandHandler("set_quantity", set_quantity))
    dp.add_handler(CommandHandler("set_increment", set_increment))
    dp.add_handler(CommandHandler("set_crypto", set_crypto))
    dp.add_handler(CommandHandler("set_time_frame", set_time_frame))
    dp.add_handler(CommandHandler("set_rsi_periode", set_rsi_periode))
    # dp.add_handler(CommandHandler("set_api_key", set_api_key))
    # dp.add_handler(CommandHandler("set_secret_key", set_secret_key))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("hello", hello))
    
    

    # Pour gérer les autres messages qui ne sont pas des commandes
    dp.add_handler(MessageHandler(Filters.text, message))

    # Sert à lancer le bot
    updater.start_polling()

    # Pour arrêter le bot proprement avec CTRL+C
    updater.idle()