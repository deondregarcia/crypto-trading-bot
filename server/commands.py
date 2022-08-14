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


def post_request(uri_path, data, api_key, api_sec):
    """Attaches auth headers and returns results of a POST request"""
    headers = {}
    headers["X-MBX-APIKEY"] = api_key
    signature = get_signature(data, api_sec)
    payload = {
        **data,
        "signature": signature,
    }
    req = requests.post((api_url + uri_path), headers=headers, data=payload)
    return req.text  # signed post request


def get_request(uri_path, data, api_key, api_sec):
    """Attaches auth headers and returns results of a POST request"""
    headers = {}
    headers["X-MBX-APIKEY"] = api_key
    signature = get_signature(data, api_sec)
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
        "timestamp": int(
            round(time.time() * 1000) - 1000
        ),  # subtract 1000 because timestamp is 1000ms ahead of binance servers; remove " - 1000" if further problems
    }
    result = get_request(uri_path, data, config.api_key, config.api_secret)
    return result
    # pprint.pprint(json.loads(result))


# test_order("DOGEUSD", "BUY", "MARKET", 200)
# get_account_info()
