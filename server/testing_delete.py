import requests, pprint

api_url = "https://api.binance.us"
symbol = "DOGEUSD"
interval = "1m"

r = requests.get(api_url + "/api/v3/klines?symbol=" + symbol + "&interval=" + interval)
# pprint.pprint(r.json())
print(len(r.json()))
