"""
Primary module for charts

This module contains the chart class for the stock portfolio engine.

Daisy Shu
May 3rd, 2020
"""

from stock import *
from portfolio import *
from datetime import date
import pandas as pd
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib as mpl
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class Chart():
    """
    Creates charts for stock interested.

    Args:
        symbol      string; ticker symbol of the stock interested
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def historical_data_chart(self):
        period1 = minus_ten_years()
        period2 = str(date.today())
        stock = web.get_data_yahoo(self.symbol, period1, period2)
        stock['Adj Close'].plot()
        plt.xlabel("Date")
        plt.ylabel("Adjusted Closing Price")
        plt.title(self.symbol + " Historical Price Data")
        plt.show()

    def portfolio_stock_returns(self):
        stock_list = Portfolio().get_stock_list()
        period1 = minus_ten_years()
        period2 = str(date.today())
        stocks = web.get_data_yahoo(stock_list, period1, period2)
        stocks_daily_returns = stocks['Adj Close'].pct_change()
        stocks_monthly_returns = stocks['Adj Close'].resample('M').ffill().pct_change()

        daily = (stocks_daily_returns + 1).cumprod().plot()
        daily.set_xlabel("Date")
        daily.set_ylabel("Growth of $1 Investment")
        daily.set_title("Your Stock Portfolio Daily Cumulative Returns Data")

        monthly = (stocks_monthly_returns + 1).cumprod().plot()
        monthly.set_xlabel("Date")
        monthly.set_ylabel("Growth of $1 Investment")
        monthly.set_title("Your Stock Portfolio Monthly Cumulative Returns Data")
        plt.show()