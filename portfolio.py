"""
Primary module for portfolio

This module contains the portfolio class for the stock portfolio engine.

Daisy Shu
May 3rd, 2020
"""

from command import *
from stock import *
from colors import *
import time

def listToString(lst):
    """
    Converts any list into a pretty formatted string.

    Output:
        string      string
    """
    if not lst:
        return ""
    elif len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return lst[0] + " and " + lst[1]
    else:
        return ', '.join(lst[:-1]) + ", and " + lst[-1]

class Portfolio(object):
    """
    Adds and removes specific stocks, as well as displays all the calculations from
    a user's personalized stock portfolio.

    Input:
        pfDict      dict; portfolio dictionary that contains a list of stocks
    """

    def __init__(self, pfDict={"stockList": []}):
        self.pfDict = pfDict

    def addStock(self, symbol):
        """
        Adds symbol of stock interested to the stock list in user's portfolio only if
        the stock does not already exist in the portfolio. If it exists, do nothing.
        The stock list should not have any duplicates.
        
        Output:
            pfDict     dict; portfolio dictionary that contains a list of stocks
        """
        stockList = self.pfDict["stockList"]
        if capitalize(symbol) in stockList:
            print(Colors.blue + "\n" + symbol + " already exists in your stock portfolio.\n" + Colors.end)
            return self.pfDict
        else:
            stockList = stockList.append(capitalize(symbol))
            print(Colors.blue + "\nYou added " + symbol + " to your portfolio.\n" + Colors.end)
            return self.pfDict

    def removeStock(self, symbol):
        """
        Removes symbol of stock interested from the stock list in user's portfolio only if
        the stock exists in the portfolio. If it doesn't exist, do nothing. The stock list
        should not have any duplicates.

        Output:
            pfDict     dict; portfolio dictionary that contains a list of stocks
        """
        stockList = self.pfDict["stockList"]
        if capitalize(symbol) in stockList:
            stockList = stockList.remove(capitalize(symbol))
            print(Colors.blue + "\nYou removed " + symbol + " from your portfolio.\n" + Colors.end)
            return self.pfDict
        else:
            print(Colors.blue + "\nYou cannot remove " + symbol + " because it is not in your stock portfolio.\n" + Colors.end)
            return self.pfDict


    def printPortfolio(self):
        """
        Prints the user's current portfolio when users type in menu command "portfolio".

        Output:
            portfolio     string; contents of user's current portfolio
        """
        stockList = self.pfDict["stockList"]
        if len(stockList) == 0:
            print("Your stock portfolio is currently empty. Add more stocks to see your portfolio data!\n")
        else:
            print(Colors.bold + Colors.purple + "\nThis is your current portfolio:\n" + Colors.end +
                "\nStocks: " + listToString(stockList) +
                "\nExpected Returns: " +
                "\nSharpe Ratio: " +
                "\nVariance: \n"
                )