import requests, pprint

api_url = "https://api.binance.us"
symbol = "ETHUSD"
interval = "1m"

r = requests.get(api_url + "/api/v3/klines?symbol=" + symbol + "&interval=" + interval)
# pprint.pprint(r.json())
list1 = []
list1.append(float(r.json()[-1][4]))
for i in range(35):
    data = r.json()[-(i + 1)][4]
    list1.append(float(data))

print(f"close time: {r.json()[-1][6]}")
list1.reverse()

print(list1)
