import websocket, json, pprint
from binance.client import Client
import config

client = Client(config.api_key, config.api_secret, tld="us")

# variable values

symbol = "dogeusdt"
interval = "1m"
stream = "/ws/" + symbol + "@kline_" + interval
# socket = "wss://stream.binance.us:9443" + stream
socket = "wss://stream.binance.com:9443" + stream

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
    candle_close = candle_info["c"]

    if is_candle_closed:
        print(candle_close)


ws = websocket.WebSocketApp(
    socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close
)
ws.run_forever()
