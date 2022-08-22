# Buy, Sell, etc. instructions
import urllib.parse
import hashlib
import hmac
import base64
import requests
import time
import config
import pprint, json


api_url = "https://api.binance.us"


def get_signature(data, secret):
    """Create and encode hmac signature for BinanceUS; used in build_request function"""
    postdata = urllib.parse.urlencode(
        data
    )  # converts to ASCII chars since only those can be sent over the internet
    message = postdata.encode()
    byte_key = bytes(secret, "UTF-8")
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()  # create hmac
    return mac


def post_request(uri_path, data):
    """Attaches auth headers and returns results of a POST request"""
    headers = {}
    headers["X-MBX-APIKEY"] = config.api_key
    signature = get_signature(data, config.api_secret)
    payload = {
        **data,
        "signature": signature,
    }
    req = requests.post((api_url + uri_path), headers=headers, data=payload)
    return req.text  # signed post request


def get_request(uri_path, data):
    """Attaches auth headers and returns results of a POST request"""
    headers = {}
    headers["X-MBX-APIKEY"] = config.api_key
    signature = get_signature(data, config.api_secret)
    params = {
        **data,
        "signature": signature,
    }
    req = requests.get((api_url + uri_path), params=params, headers=headers)
    return req.text  # signed get request


def test_order(symbol, side, type, quantity):
    """Send test order; response should be {}"""
    uri_path = "/api/v3/order/test"
    data = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "quantity": quantity,
        "timestamp": int(round(time.time() * 1000)),
    }
    result = post_request(uri_path, data, config.api_key, config.api_secret)
    print("POST {}: {}".format(uri_path, result))


def get_account_info():
    """Pulls balances and statuses for account"""
    uri_path = "/api/v3/account"
    data = {
        "timestamp": int(round(time.time() * 1000) - 1000)
        - 1000,  # subtract 1000 because timestamp is 1000ms ahead of binance servers; remove " - 1000" if further problems
    }
    result = get_request(uri_path, data)
    return result
    # pprint.pprint(json.loads(result))


def get_trade_history(symbol):
    """Pulls trade history for a specific coin"""
    uri_path = "/api/v3/myTrades"
    data = {
        "timestamp": int(round(time.time() * 1000) - 1000) - 1000,
        "symbol": symbol,
    }
    result = get_request(uri_path, data)
    return result


print(get_trade_history("DOGEUSD"))

# implement method of finding quantity amounts for a specific crypto based on percentage of total USD balance
#   - i.e. with my balance of $100, i can spend 20% on one order if i buy x quantity of doge coin
def buy_market(symbol, quantity):
    """Executes a MARKET-type buy order"""
    uri_path = "/api/v3/order"
    data = {
        "symbol": symbol,
        "side": "BUY",
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(round(time.time() * 1000) - 1000),
    }
    order = post_request(uri_path, data)
    return order


# implement a way to automatically find total quantity in order to execute a complete exit
def sell_market(symbol, quantity):
    """Executes a MARKET-type sell order"""
    uri_path = "/api/v3/order"
    data = {
        "symbol": symbol,
        "side": "SELL",
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(round(time.time() * 1000) - 1000),
    }
    order = post_request(uri_path, data)
    print(order)


# find a way to automatically calculate stopPrice, e.g. 5% below buy price
def sell_stop_loss_market(symbol, quantity, stopPrice):
    """Executes a stop loss, market sell order (as opposed to stop loss, limit sell order)"""
    uri_path = "/api/v3/order"
    data = {
        "symbol": symbol,
        "side": "SELL",
        "type": "STOP_LOSS",
        "quantity": quantity,
        "stopPrice": stopPrice,
        "timestamp": int(round(time.time() * 1000) - 1000),
    }
