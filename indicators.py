# All the technical indicators to be used in the strategies.py file

import numpy as np

# testing_array = [10, 11, 14, 16, 12, 14]
testing_array = [10, 11, 14, 16, 12]


def simple_moving_average(array, periods):
    """avg of # periods"""
    array_copy = array.copy()
    temp_array = []
    for i in range(periods):
        value = array_copy.pop()
        temp_array.append(value)
    a = np.array(temp_array)
    return np.mean(a)


def exponential_moving_average(array, periods):
    """simple moving average with more weight on recent data"""

    # format numpy array
    array_copy = array.copy()
    temp_array = []
    for i in range(periods + 1):
        value = array_copy.pop()
        temp_array.append(value)
    a = np.array(temp_array)

    # calc weighted multiplier
    wm = 2 / (periods + 1)
    print(f"length of a: {len(a)}")

    # if len(a) <= ((periods - 1) / 2):

    # if len(a) < periods + 1:
    #     return
    # elif (
    #     len(a) == periods + 1
    # ):  # use SMA as EMA(yesterday) for first entry since EMA(y) does not exist yet
    #     sma = np.mean(a)
    #     return (array[-1] * wm) + (sma * (1 - wm))
    # else:
    #     price_today = array[-1]
    #     new_array = array.pop()
    #     return (price_today * wm) + (
    #         exponential_moving_average(new_array, periods) * (1 - wm)
    #     )


# print(f"SMA: {simple_moving_average(testing_array, 5)}")

answer = exponential_moving_average(testing_array, 3)
print(answer)
