import websocket, json, pprint, numpy

from indicators import *
import config, strategies

api_url = "https://api.binance.us"

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
# coin = "dogeusd"
coin = "ethusd"
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
