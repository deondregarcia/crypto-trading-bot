import requests, pprint

api_url = "https://api.binance.us"
symbol = "ETHUSD"
interval = "1m"

r = requests.get(api_url + "/api/v3/klines?symbol=" + symbol + "&interval=" + interval)
# pprint.pprint(r.json())
list1 = []
list1.append(r.json()[-1][4])
for i in range(35):
    list1.append(r.json()[-(i + 1)][4])

print(f"start time: {r.json()[-1][0]}")
list1.reverse()
print(list1)
