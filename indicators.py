# All the technical indicators to be used in the strategies.py file
import numpy as np

# testing_array = [23, 42, 76, 2, 11]
testing_array = [
    10,
    11,
    14,
    16,
    12,
    23,
    42,
    76,
    2,
    11,
    23,
    46,
    43,
    76,
    23,
    78,
    54,
    76,
    32,
    45,
    67,
    32,
    67,
    13,
    9,
    12,
    6,
    12,
    56,
    78,
    45,
    98,
    47,
    32,
    67,
    13,
    9,
    12,
    6,
    12,
    56,
    78,
    45,
    98,
    47,
]


def simple_moving_average(array, periods):
    """avg of # periods"""
    start_index = len(array) - periods  # starting index of array based on periods value
    return np.mean(array[start_index:])


def exponential_moving_average(array, periods):
    """simple moving average with more weight on recent data"""
    if len(array) == periods:  # base case
        # print(f"len(array): {len(array)}, periods: {np.ceil(((periods - 1) / 2))}")
        print(f"mean: {np.mean(array)}")
        # print(array)
        return np.mean(array)
    else:
        wm = 2 / (periods + 1)  # calc weighted multiplier
        price_today = array[-1]
        print(f"price_today: {price_today}")
        new_array = array[:-1]
        print(f"new_array: {new_array}")
        # recursive formula
        return price_today * wm + exponential_moving_average(new_array, periods) * (
            1 - wm
        )


# ---------------------NEED TO FIX: returning values that are too low for dogeusd stream, correct this--------------------------------------
def MACD(array, fast_periods, slow_periods, macd_periods):
    """Example Usage: MACD([array], 12, 26, 9)"""
    if len(array) < 35:
        print("Need at least 35 periods to calculate MACD")
        return
    else:

        def MACD_loop(arr, fast_p, slow_p):
            """MACD called several times to find signal line, prevents too many function calls"""
            fast_ema = exponential_moving_average(arr, fast_p)
            slow_ema = exponential_moving_average(arr, slow_p)
            return fast_ema - slow_ema

        macd = MACD_loop(array, fast_periods, slow_periods)
        macd_array = [macd]
        for i in range(1, macd_periods):
            macd_array.append(
                MACD_loop(array[: -(1 * i)], fast_periods, slow_periods)
            )  # array[:-(1 * i)] consecutively returns array after slicing off last element

        print(f"macd_array: {macd_array}")

        signal_line = exponential_moving_average(macd_array, macd_periods)
        return [macd, signal_line]


def bollinger_bands(array, periods):
    """
    returns inner sma line and outer std. dev. bands
    typically used with a 20 day SMA
    """
    sma = simple_moving_average(array, periods)
    std_dev = np.std(array)
    upper_band = sma + (std_dev * 2)
    lower_band = sma - (std_dev * 2)

    return [upper_band, sma, lower_band]


def relative_strength_index(array, periods):
    """standard # of periods is 14"""
    # avg_gain =


# print(exponential_moving_average(testing_array, 12))
# print(simple_moving_average(testing_array, 3))
# print(MACD(testing_array, 12, 26, 9))
print(bollinger_bands(testing_array, 20))
