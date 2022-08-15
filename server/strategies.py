# hold all the strategies and Crypto class
from indicators import *
from test_arrays import *

# create Python class for each crypto being tracked later on
# class Crypto:
#     def __init__(self, close_array):
#         self.close_array = []


# ----------------------------- LOOK INTO RANGE TRADING ----------------------------------------------
#   https://thesensibleguidetoforex.com/2014/03/19/4-rules-for-using-double-bollinger-bands-the-most-useful-technical-indicator-part-1/

# first strategy:
# combination of SMA or MACD, RSI, Bollinger Bands
# for bollinger bands, add an immediate sell condition if price drops below

# Double Bollinger Band Signal Notes
#   - use standard deviation of either 0.5 and 3 or 1 and 2
#   - between 1 and 2 is buy signal, between -1 and -2 is sell signal, between 1 and -1 is neutral zone


# NOTES:
#   - All functions return nothing if there is no signal


def DBB_signal(array, periods, first_std_dev, second_std_dev):
    """Sell signal if price closes between lower first and second bands; Buy signal if price closes between upper first and second"""
    # price_close = double_bollinger_bands(array, periods, first_std_dev, second_std_dev)
    [upper2, upper1, lower1, lower2] = double_bollinger_bands(
        array, periods, first_std_dev, second_std_dev
    )

    # def check_range(closing_price):
    #     if closing_price > upper1 and closing_price

    if array[-1] > upper1:
        for i in range(2):
            if array[-(1 * (i + 2))] > upper1:
                print("above upper1")
                continue
            else:
                return
        return "BUY"
    elif array[-1] < lower1:
        for i in range(2):
            if array[-(1 * (i + 2))] < lower1:
                print("below lower1")
                continue
            else:
                return
        return "SELL"
    else:
        return


def RSI_signal(array, periods):
    """Returns BUY signal when above 70, SELL when below 30"""
    # RSI measures speed and magnitude of recent price changes
    # best for trading ranges rather than markets
    rsi = relative_strength_index(array, periods)

    if rsi > 70:
        return "SELL"
    elif rsi < 30:
        return "BUY"
    else:
        return


def MACD_signal(array, fast_periods, slow_periods, macd_periods):
    """
    Returns BUY/SELL signal when MACD crosses over signal line and remains there for 3 crosses
    """
    [macd_array, signal_line] = MACD(array, fast_periods, slow_periods, macd_periods)

    above_signal = None

    #   ---- what if the starting value is a line that just barely crosses and hovers over
    #   ---- the signal line, then dips back down. Current code counts that as a crossover,
    #   ---- need to find a solution for that edge case.
    #   ---- weighting?

    # look back at last int(macd_periods) closes and see if crossover occurred
    if macd_array[0] > signal_line:
        cross_counter = 0
        # later on, calculate velocity and magnitude of cross for better insights
        for i in range(1, macd_periods):
            if macd_array[i] < signal_line:  # if less than, there exists a cross
                cross_counter += 1
            if cross_counter >= 3:
                return "SELL"
    elif macd_array[0] < signal_line:
        cross_counter = 0
        for i in range(1, macd_periods):
            if macd_array[i] > signal_line:
                cross_counter += 1
            if cross_counter >= 3:
                return "BUY"
    else:
        return


# DBB_strat(eth_array_2_from_binance, 20, 1, 2)
