# All the technical indicators to be used in the strategies.py file
# from tracemalloc import start --removed this, see if it pops up again automatically
import numpy as np
import pandas as pd
from test_arrays import *


def simple_moving_average(array, periods):
    """avg of # periods"""
    start_index = len(array) - periods  # starting index of array based on periods value
    return np.mean(array[start_index:])


def exponential_moving_average(array, periods):
    """moving average with more weight on recent data"""
    if len(array) < periods:
        print("Must have periods + 1 number of inputs for EMA")
        return
    elif len(array) == periods:  # base case
        return np.mean(array)
    else:
        print("ema test")
        wm = 2 / (periods + 1)  # calc weighted multiplier
        price_today = array[-1]
        new_array = array[:-1]
        # recursive formula
        return price_today * wm + exponential_moving_average(new_array, periods) * (
            1 - wm
        )


def smoothed_moving_average(array, periods):
    """similar to EMA with different weighted multiplier; moving average with alpha = 1/N smoothing"""
    if len(array) < periods:
        print("Must have periods + 1 number of inputs for EMA")
        return
    elif len(array) == periods:  # base case
        return np.mean(array)
    else:
        wm = 1 / (periods)  # calc weighted multiplier
        price_today = array[-1]
        new_array = array[:-1]
        # recursive formula
        return price_today * wm + smoothed_moving_average(new_array, periods) * (1 - wm)


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
        return [f"macd: {macd}", f"signal line: {signal_line}"]


def bollinger_bands(array, periods):
    """
    returns inner sma line and outer std. dev. bands
    typically used with a 20 day SMA
    """
    if len(array) < periods:
        print(f"Need {periods} for Bollinger Bands")
        return
    else:
        sma = simple_moving_average(array, periods)
        std_dev = np.std(array)
        upper_band = sma + (std_dev * 2)
        lower_band = sma - (std_dev * 2)

        return [upper_band, sma, lower_band]


def relative_strength_index(array, periods):
    """
    standard # of periods is 14, but fast/minute charts might not be good for RSI
    This RSI uses Wilder's SMMA for its smoothing alpha
    """
    if len(array) < periods:
        print(f"Need at least {periods} closes for RSI")
        return
    else:
        gains = []
        losses = []

        # separate positive price changes from the negative ones for all price changes in array, then only calculate the 'periods' amount later
        for i in range(0, len(array) - 1):
            price_change = array[i + 1] - array[i]
            if price_change > 0:
                gains.append(price_change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(price_change))

        # calculate the SMMA only for the 'periods' amount
        avg_gains = smoothed_moving_average(gains, periods)
        avg_losses = smoothed_moving_average(losses, periods)
        relative_strength = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + relative_strength))
        return rsi


# print(simple_moving_average(testing_array, 3))
# print(MACD(eth_array_2_from_binance, 12, 26, 9))
# print(bollinger_bands(eth_array_2_from_binance, 21))
# relative_strength_index(eth_array_2_from_binance, 14)
# print(exponential_moving_average(eth_array_2_from_binance, 12))
