import requests, pprint
import time
from datetime import datetime
from strategies import *

api_url = "https://api.binance.us"
symbol = "ETHUSD"
# interval = "1m"
interval = "30m"

# pprint.pprint(r.json())

# multiply by 1000 because Binance timestamp operates in milliseconds
current_time = int(round(time.time())) * 1000

# subtract by 60,000,000 milliseconds to get the time 16Hours40Minutes ago to reach 1000 inputs for the 1m interval
start_time = str(current_time - 60000000)


r = requests.get(
    api_url
    + "/api/v3/klines?symbol="
    + symbol
    + "&interval="
    + interval
    # + "&startTime="
    # + str(start_time)
    # + "&limit="
    # + str(1000)
)


data = r.json()

# time = int(round(data[0][6]))
# print(datetime.fromtimestamp(time / 1000).strftime("%Y-%m-%d %H:%M:%S"))
# print(data)


inputs = []

for i in range(len(data)):
    inputs.append(float(data[i][4]))
    # time = int(round(data[i][6]))
    # print(datetime.utcfromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S"))
    # print(datetime.fromtimestamp(time / 1000).strftime("%Y-%m-%d %H:%M:%S"))

# pprint.pprint(inputs)

# print(r.json()[0][4])

# print(inputs)
slow = 0
fast = 15
# print(len(inputs[slow:fast]))
while fast <= len(inputs):
    print(RSI_signal(inputs[slow:fast], 14))
    slow += 1
    fast = slow + 15
print(inputs[-2])
# print(f"len(inputs): {len(inputs)} ")
# print(f"slow: {slow} ")
# print(f"fast: {fast} ")
