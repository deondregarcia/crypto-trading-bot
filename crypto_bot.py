import websocket, json, pprint, talib, numpy
from binance.client import Client
import config, strategies

client = Client(config.api_key, config.api_secret, tld="us")

# list of 10 coins to keep track of
# bitcoin, ethereum, doge coin, BNB (binance coin), cardano (ADA), polygon (MATIC), BarnBridge (BOND), AVALANCHE AVAX, ApeCoin (APE), Chainlink (LINK)
# 4

# ideas for the program:
# ***   develop some algorithm to analyze past and current price action as a human would (watch videos, etc.)
# partial pullouts on runs: in order to maximize runs, take out small amounts to ensure i make money back (rather than selling all at once)
# ***   backtesting
# minimum 5 strats
# manual forced buys and forced sells
# maybe track large volumes of coins (dozens)
# ***   maybe invest small amounts across many coins
# remember position sizing and risk management
# ****  website with weekly reports on performance, history view of all trades and trades run with particular strats for comparison,
# --    interface to activate code from web, maybe run python script in browser, list and charts of my selected coins on web
# iphone notifications?
# ***   remote activation and deactivation from my phone
# ***   need to examine and implement order types

# variable values

coin_list = [
    "dogeusd",
    "btcusd",
    "ethusd",
    "bnbusd",
    "avaxusd",
    "adausd",
    "maticusd",
    "bondusd",
    "apeusd",
    "linkusd",
    "etcusd",
]

interval = "1m"

# not /ws/ because / added in below loop
stream = "/ws"
for coin in coin_list:
    stream += "/" + coin + "@kline_" + interval

# stream = "/ws/" + stream + "@kline_" + interval
socket = "wss://stream.binance.us:9443" + stream
# socket = "wss://stream.binance.com:9443" + stream

print(socket)


def on_open(ws):
    print("Opened connection")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("Closed connection")


def on_message(ws, message):
    json_message = json.loads(message)
    # pprint.pprint(json_message)
    candle_info = json_message["k"]

    is_candle_closed = candle_info["x"]
    candle_symbol = candle_info["s"]
    candle_interval = candle_info["i"]
    candle_close = candle_info["c"]

    if is_candle_closed:
        print(
            "{} {} candle closed at {}".format(
                candle_symbol, candle_interval, candle_close
            )
        )


ws = websocket.WebSocketApp(
    socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close
)
ws.run_forever()
