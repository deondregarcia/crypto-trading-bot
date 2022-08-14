import websocket, json, pprint, numpy

# from binance.client import Client
# from binance.enums import *
from indicators import *
import config, strategies

api_url = "https://api.binance.us"

# client = Client(config.api_key, config.api_secret, tld="us")

# ----------------------- look into using pandas per this link: https://www.alpharithms.com/calculate-macd-python-272222/ --------------------------

# list of 10 coins to keep track of
# bitcoin, ethereum, doge coin, BNB (binance coin), cardano (ADA), polygon (MATIC), BarnBridge (BOND), AVALANCHE AVAX, ApeCoin (APE), Chainlink (LINK)
# 4

# Overall tentative plan, based on ideas below:
#   - python cryptocurrency trading bot
#   - web app that has charts, UI buttons to execute code for python cryptocurrency bot
#   - database for storing past results, and corresponding chart to graph results. Visible to everyone.

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

# # not /ws/ because / added in below loop
# stream = "/ws"
# for coin in coin_list:
#     stream += "/" + coin + "@kline_" + interval

# socket = "wss://stream.binance.us:9443" + stream

coin = "dogeusd"
stream = "/ws/" + coin + "@kline_" + interval
socket = "wss://stream.binance.us:9443" + stream

print(socket)


def on_open(ws):
    print("Opened connection")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("Closed connection")


close_array = []


def on_message(ws, message):
    json_message = json.loads(message)
    candle_info = json_message["k"]

    is_candle_closed = candle_info["x"]
    candle_symbol = candle_info["s"]
    candle_interval = candle_info["i"]
    candle_close = candle_info["c"]

    # test order worked; returns {}
    # order = client.create_test_order(
    #     symbol="DOGEUSD",
    #     side=SIDE_BUY,
    #     type=ORDER_TYPE_LIMIT,
    #     timeInForce=TIME_IN_FORCE_GTC,
    #     quantity=200,
    #     price="0.071",
    # )
    # print(order)

    print(f"close_array: {close_array}")
    close_array.append(float(candle_close))
    print(MACD(close_array, 12, 26, 9))
    # if is_candle_closed:
    #     print(
    #         "{} {} candle closed at {}".format(
    #             candle_symbol, candle_interval, candle_close
    #         )
    #     )


ws = websocket.WebSocketApp(
    socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close
)

# ws.run_forever()
# ws.close()


def start_bot():
    ws.run_forever()


def stop_bot():
    ws.close()
