# All the technical indicators to be used in the strategies.py file
import numpy as np

# testing_array = [23, 42, 76, 2, 11]
testing_array = [10, 11, 14, 16, 12]


def simple_moving_average(array, periods):
    """avg of # periods"""
    start_index = len(array) - periods  # starting index of array based on periods value
    return np.mean(array[start_index:])


def exponential_moving_average(array, periods):
    """simple moving average with more weight on recent data"""
    if len(array) <= ((periods - 1) / 2):  # base case
        return np.mean(array)
    else:
        wm = 2 / (periods + 1)  # calc weighted multiplier
        price_today = array[-1]
        new_array = array[:-1]
        # recursive formula
        return (price_today * wm) + (
            exponential_moving_average(new_array, periods) * (1 - wm)
        )


print(exponential_moving_average(testing_array, 3))
print(simple_moving_average(testing_array, 3))
