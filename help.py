"""
Primary module for help command in menu

This module contains functions for the engine's help manual.

Daisy Shu
May 3rd, 2020
"""

class NoAnswer(Exception):
    """
    Raised when the help manual does not have an answer to the question
    asked.
    """
    pass

def intersection(input, key_word_list, word_options_list):
    question = lower(input).strip()
    question = question.replace("?", "")
    question_list = question.split()
    bool_list = []
    for word in question_list:
        true_false = word in word_options_list
        bool_list.append(true_false)
    return set(key_word_list).issubset(question_list) and (True in bool_list)

def help_manual(input):
    previous_close =    ["previous", "close"]
    previous_closing =  ["previous", "closing"]
    market_cap =        ["market", "cap"]
    beta =              ["beta"]
    pe_ratio =          ["pe", "ratio"]
    eps =               ["eps"]
    ttm =               ["ttm"]
    expected_return =   ["expected", "return"]
    volatility =        ["volatility"]
    variance =          ["variance"]
    var_vol =           ["variance", "volatility"]
    sharpe_ratio =      ["sharpe", "ratio"]

    historical_data =   ["historical", "data"]
    adjusted_close =    ["adjusted", "close"]
    adjusted_closing =  ["adjusted", "closing"]
    adj_close =         ["adj", "close"]
    closing_price =     ["closing", "price"]
    annualized =        ["annualized"]

    optimize =          ["optimize", "portfolio"]

    type_help =         ["help"]

    what =              ["what", "whats", "what's"]
    how =               ["how"]
    difference =        ["different", "difference"]

    if intersection(input, previous_close, what) or\
    intersection(input, previous_closing, what):
        print("\nPrevious closing price is the prior day's final stock price"
        + " when the market officially closes for the day.")
    elif intersection(input, market_cap, what):
        print("\nMarket cap, or market capitalization, is the total value"
        + " of all a company's shares of stock.")
    elif intersection(input, beta, what):
        print("\nBeta is a measure of a stock's volatility in relation to"
        + " the overall market. A beta above 1.0 means the stock moves more"
        + " than the market over time. A beta less than 1.0 means the stock"
        + " moves less than the market.")
    elif intersection(input, pe_ratio, what):
        print("\nP/E ratio, or price-earnings ratio, is the ratio of a"
        + " company's share price to the company's earnings per share"
        + " (EPS). The ratio is used for valuing companies and to determine"
        + " whether they are overvalued or undervalued.")
    elif intersection(input, eps, what):
        print("\nEPS, or earnings per share, is a company's profit divided"
        + " by the outstanding shares of its common stock.")
    elif intersection(input, ttm, what):
        print("\nTTM stands for trailing twelve months, and is a term used"
        + " to describe the past 12 consecutive months of a company’s"
        + " performance data.")
    elif intersection(input, expected_return, what):
        print("\nExpected return is the profit or loss you anticipate on an"
        + " investment. In this case, the profit or loss on your portfolio.")
    elif intersection(input, volatility, what):
        print("\nVolatility is a statistical measure of the dispersion of"
        + " returns for an investment. In most cases, the higher the"
        + " volatility, the riskier the investment, or in this case, your"
        + " portfolio.")
    elif intersection(input, variance, what):
        print("\nVariance is a measurement of the degree of risk in an"
        + " investment. Variance of the returns among assets in a"
        + " portfolio is analyzed as a means of achieving the best asset"
        + " allocation.")
    elif intersection(input, var_vol, difference):
        print("\nThe difference between variance and volatility is that"
        + " variance is a measure of distribution of returns and is not"
        + " neccesarily bound by any time period. Volatility is a measure"
        + " of the standard deviation (square root of the variance) over"
        + " a certain time interval. Variance and volatility both gives"
        + " you a sense of an asset's risk.")
    elif intersection(input, sharpe_ratio, what):
        print("\nA Sharpe ratio is the performance of an investment compared"
        + " to a risk-free asset, after adjusting for its risk. It helps"
        + " investors understand the return of an investment compared to"
        + " its risk. Generally, the greater the Sharpe ratio, the greater"
        + " the risk-adjusted return.")
    elif intersection(input, historical_data, what):
        print("\nHistorical data is information about a company's past, such"
        + " as its revenues, earnings, and stock price action. The"
        + " historical data outputted by this engine is from 10"
        + " years ago, or the most recent data if data from 10 years ago is"
        + " not available.")
    elif intersection(input, adjusted_close, what) or \
    intersection(input, adjusted_closing, what) or \
    intersection(input, adj_close, what):
        print("\nAdjusted closing price adjusts a stock's closing price to"
        + " accurately reflect that stock's value after accounting for any"
        + " corporate actions.")
    elif intersection(input, closing_price, what):
        print("\nClosing price is the 'raw' price which is just the cash"
        + " value of the last transacted price before the market closes.")
    elif intersection(input, annualized, what):
        print("\nAnnualized means converting a short-term rate of return"
        + " or volatility to an annual rate of return or volatility.")
    elif intersection(input, optimize, how):
        print("\nTo optimize your portfolio, simply type 'optimize"
        + " portfolio' in the main menu. This engine will then optimize"
        + " your portfolio in two ways: 1) By maximizing your portfolio's"
        + " Sharpe ratio and 2) By minimizing your portfolio's volatility"
        + " or risk.")
    elif intersection(input, type_help, type_help):
        print("\nYou have already activated the help command. Please type a"
        + " question below:")
    else:
        raise NoAnswer

def lower(str):
    """
    Returns string [str] lowercase.

    Args:
        str                 string
    Returns:
        lowercase_str       string
    """
    return str.lower()