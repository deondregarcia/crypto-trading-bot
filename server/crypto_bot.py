import websocket, json, pprint, numpy

from indicators import *
import config, strategies

api_url = "https://api.binance.us"


# Goals for tomorrow, Aug 14:
#   - write func to check account balance --DONE
#   - test out the RSI and bollinger band indicators, eth since its array has a start time --DONE
#   - create my first strategy combining the MACD, RSI, and BB's to generate signals. Include percentage stop losses and trailing stop losses in the order.
#   - figure out a way to backtest the strategy (by downloading Binance API historical zip files or finding a way to do it through API, which is preferred)
#   - backtest that strategy
#   - maybe find a way to log results, idk its kind of a longer process bc i need a database then.


# ----------------------- look into using pandas per this link: https://www.alpharithms.com/calculate-macd-python-272222/ --------------------------

# list of 10 coins to keep track of
# bitcoin, ethereum, doge coin, BNB (binance coin), cardano (ADA), polygon (MATIC), BarnBridge (BOND), AVALANCHE AVAX, ApeCoin (APE), Chainlink (LINK)
# 4

# Overall tentative plan, based on ideas below:
#   - python cryptocurrency trading bot
#   - web app that has charts, UI buttons to execute code for python cryptocurrency bot
#   - statistics on the overall performance of my bot and each strategy in particular
#   - database for storing past results, and corresponding chart to graph results. Visible to everyone.

# Strategy:
#   - go a little overkill on some of the indicators; play for limited, safe transactions since I don't have to pay attention to the markets myself

# Notes for Improvement:
#   - for the EMA and SMMA, and therefore for the RSI, MACD, etc. which depend on them, the functions calculate ALL values in the array in order to reach base case,
#   so the longer the bot runs, the longer the input arrays get, the slower the performance. Could increase this by caching the return values.

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

# ------ multiple streams ------
# # not /ws/ because / added in below loop
# stream = "/ws"
# for coin in coin_list:
#     stream += "/" + coin + "@kline_" + interval
# socket = "wss://stream.binance.us:9443" + stream

# single stream
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

    if is_candle_closed:
        close_array.append(float(candle_close))
        print(f"close_array: {close_array}")
        print(f"MACD: {MACD(close_array, 12, 26, 9)}")
        print(f"Bollinger Bands: {bollinger_bands(close_array, 20)}")
        print(f"RSI: {relative_strength_index(close_array, 14)}")


ws = websocket.WebSocketApp(
    socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close
)


def start_bot():
    ws.run_forever()


def stop_bot():
    ws.close()
