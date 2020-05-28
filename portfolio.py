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

class WeightsMismatch(Exception):
    """
    Raised when total number of weights don't match the number of stocks
    in user's current portfolio.
    """
    pass

class WeightsMiscalculation(Exception):
    """
    Raised when total weights entered do not add up to 1.
    """
    pass

class WeightsMalformed(Exception):
    """
    Raised when weights are malformed. For example, weights that contain
    letters would be deemed malformed.
    """
    pass

def list_to_string(lst):
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
    Adds and removes specific stocks, as well as displays all the
    calculations from a user's personalized stock portfolio.

    Input:
        pf_dict     dict; portfolio dictionary that contains a list of
                    stocks
    """

    def __init__(self, pf_dict={"Stock List": []}):
        self.pf_dict = pf_dict

    def get_stock_list(self):
        return self.pf_dict["Stock List"]

    def add_stock(self, symbol):
        """
        Adds symbol of stock interested to the stock list in user's portfolio
        only if the stock does not already exist in the portfolio. If it
        exists, do nothing. The stock list should not have any duplicates.
        
        Output:
            pf_dict     dict; portfolio dictionary that contains a list of
                        stocks
        """
        stock_list = self.get_stock_list()
        if capitalize(symbol) in stock_list:
            print(Colors.blue + "\n" + symbol
            + " already exists in your stock portfolio.\n" + Colors.end)
            return self.pf_dict
        else:
            stock_list = stock_list.append(capitalize(symbol))
            print(Colors.blue + "\nYou added " + symbol
            + " to your portfolio.\n" + Colors.end)
            return self.pf_dict

    def remove_stock(self, symbol):
        """
        Removes symbol of stock interested from the stock list in user's
        portfolio only if the stock exists in the portfolio. If it doesn't
        exist, do nothing. The stock list should not have any duplicates.

        Output:
            pf_dict     dict; portfolio dictionary that contains a list of
                        stocks
        """
        stock_list = self.get_stock_list()
        if capitalize(symbol) in stock_list:
            stock_list = stock_list.remove(capitalize(symbol))
            print(Colors.blue + "\nYou removed " + symbol
            + " from your portfolio.\n" + Colors.end)
            return self.pf_dict
        else:
            print(Colors.blue + "\nYou cannot remove "
            + symbol + " because it is not in your stock portfolio.\n"
            + Colors.end)
            return self.pf_dict

    def convert_weights_to_array(self, weights):
        try:
            weights = weights.strip()
            weights_list = weights.split(",")
            weights_list = [x for x in weights_list[:] if x != '']
            for i in range(len(weights_list)):
                weights_list[i] = float(weights_list[i])
            return np.asarray(weights_list)
        except:
            raise WeightsMalformed

    def expected_returns_sd(self, weights):
        stock_list = self.get_stock_list()
        data = web.DataReader(stock_list, data_source="yahoo", start=minus_five_years())['Adj Close']
        data.sort_index(inplace=True)
        returns = data.pct_change()
        mean_return = returns.mean()
        covariance_matrix = returns.cov()

        portfolio_return = round(np.sum(mean_return * weights) * 252, 2)
        portfolio_sd = round(np.sqrt(np.dot(weights.T,
        np.dot(covariance_matrix, weights))) * np.sqrt(252), 2)

        return portfolio_return, portfolio_sd

    def expected_returns(self, weights):
        return self.expected_returns_sd(weights)[0]

    def expected_sd(self, weights):
        return self.expected_returns_sd(weights)[1]

    def sharpe_ratio(self, weights):
        pf_return = self.expected_returns(weights)
        pf_sd = self.expected_sd(weights)
        return round(pf_return/pf_sd, 2)

    def variance(self, weights):
        pf_sd = self.expected_sd(weights)
        return round(pf_sd**2, 2)

    def print_portfolio(self, weights):
        """
        Prints the user's current portfolio when users type in menu command
        "portfolio".

        Raises:
            WeightsMismatch             exception raised when number of
                                        weights does not match number of
                                        stocks in user's current portfolio
            WeightsMiscalculation       exception raised when weights do not
                                        add to 1

        Output:
            portfolio     string; contents of user's current portfolio
        """
        stock_list = self.get_stock_list()
        weights = self.convert_weights_to_array(weights)

        if len(weights) != len(stock_list):
            raise WeightsMismatch
        elif np.sum(weights) != 1.:
            raise WeightsMiscalculation
        else:
            print(Colors.bold + Colors.purple
            + "\nThis is your current portfolio:\n" + Colors.end
            + "\nStocks:           " + list_to_string(stock_list)
            + "\nExpected Returns: " + str(self.expected_returns(weights))
            + "\nSharpe Ratio:     " + str(self.sharpe_ratio(weights))
            + "\nVariance:         " + str(self.variance(weights)) + "\n"
            + "\nYour portfolio annualized expected return is "
            + str(self.expected_returns(weights))
            + " and portfolio annualized volatility is "
            + str(self.expected_sd(weights)) + ".\n")