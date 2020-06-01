"""
Primary module for portfolio

This module contains the portfolio class for the stock portfolio engine.

Daisy Shu
May 3rd, 2020
"""

from colors import *
from command import *
from stock import *
import time
from pypfopt.efficient_frontier import EfficientFrontier

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

    Returns:
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

    Args:
        pf_dict     dict; portfolio dictionary that contains a list of
                    stocks
    """

    def __init__(self, pf_dict={"Stock List": []}):
        self.pf_dict = pf_dict

    def get_stock_list(self):
        """
        Getter for value of 'Stock List' key in pf_dict.

        Returns:
            stock_list      string list
        """
        return self.pf_dict["Stock List"]

    def add_stock(self, symbol):
        """
        Adds symbol of stock interested to the stock list in user's portfolio
        only if the stock does not already exist in the portfolio. If it
        exists, do nothing. The stock list should not have any duplicates.
        
        Args:
            symbol      string
        Returns:
            pf_dict     dict; portfolio dictionary that contains a list of
                        stocks
        """
        try:
            url_summary = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
            params_summary = {"region": "US", "symbol": symbol}
            headers = {
                'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
                'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
                }
            response = requests.request(
                                        "GET", url_summary,
                                        headers=headers, params=params_summary
                                        )
            text = response.text
            json_text = json.loads(text)
        except:
            raise InexistentStock

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

        Args:
            symbol      string
        Returns:
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
        """
        Converts a given weights string to a numpy array.

        Args:
            weights                 string
        Returns:
            weights_list            numpy array
        Raises:
            WeightsMalformed        exception raised when weights are
                                    malformed
        """
        try:
            weights = weights.strip()
            weights_list = weights.split(",")
            weights_list = [x for x in weights_list[:] if x != '']
            for i in range(len(weights_list)):
                weights_list[i] = float(weights_list[i])
            return np.asarray(weights_list)
        except:
            raise WeightsMalformed

    def risk_free_rate(self, inflation_rate=0.018):
        """
        Calculates the current risk free rate based on government bond rate
        and inflation rate.

        Returns:
            risk_free_rate      float
        """
        return ((1.0 + get_gov_bond_rate())/(1.0 + inflation_rate)) - 1.0

    def portfolio_calculations(self, weights):
        """
        Calculates annualized expected returns, annualized expected standard
        deviation, Sharpe ratio, and variance of user's portfolio.
        
        Args:
            weights                             numpy array
        Returns:
            expected_returns, expected_sd,      tuple
            sharpe_ratio, variance
        """
        stock_list = self.get_stock_list()
        data = web.DataReader(stock_list, data_source="yahoo", \
        start=minus_ten_years())['Adj Close']
        returns = data.pct_change()
        mean_return = returns.mean()
        # there are 252 trading days for this year (2020)
        covariance_matrix = returns.cov() * 252
        
        expected_returns = round(np.sum(mean_return * weights) * 252, 2)
        variance = round(np.dot(weights.T, \
        np.dot(covariance_matrix, weights)), 2)
        expected_sd = round(np.sqrt(variance), 2)
        sharpe_ratio = round((expected_returns-self.risk_free_rate())/expected_sd, 2)

        return expected_returns, expected_sd, sharpe_ratio, variance

    def print_portfolio(self, weights):
        """
        Prints the user's current portfolio when users type in menu command
        "portfolio".

        Args:
            weights                     string
        Returns:
            portfolio                   string; contents of user's current
                                        portfolio
        Raises:
            WeightsMismatch             exception raised when number of
                                        weights does not match number of
                                        stocks in user's current portfolio
            WeightsMiscalculation       exception raised when weights do not
                                        add to 1
        """
        stock_list = self.get_stock_list()
        weights = self.convert_weights_to_array(weights)

        if len(weights) != len(stock_list):
            raise WeightsMismatch
        elif np.sum(weights) != 1.:
            raise WeightsMiscalculation
        else:
            start_time = time.time()

            expected_returns = str(self.portfolio_calculations(weights)[0])
            expected_sd = str(self.portfolio_calculations(weights)[1])
            sharpe_ratio = str(self.portfolio_calculations(weights)[2])
            variance = str(self.portfolio_calculations(weights)[3])

            print(Colors.bold + Colors.purple
            + "\nThis is your current portfolio:\n" + Colors.end
            + "\nStocks:           " + list_to_string(stock_list)
            + "\nExpected Returns: " + expected_returns
            + "\nSharpe Ratio:     " + sharpe_ratio
            + "\nVariance:         " + variance + "\n"
            + "\nYour portfolio annualized expected return is "
            + expected_returns
            + " and portfolio annualized volatility is "
            + expected_sd + ".\n")
        print("--- %s seconds ---" % (time.time() - start_time))

    def optimize_pf_max_sharpe(self):
        """
        Optimizes the user's portfolio by maximizing Sharpe ratio.

        Returns:
            expected_return, volatility,        string
            sharpe_ratio
        """
        stock_list = self.get_stock_list()
        data = web.DataReader(stock_list, data_source="yahoo", \
        start=minus_ten_years())['Adj Close']
        returns = data.pct_change()
        expected_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252

        ef = EfficientFrontier(expected_returns, cov_matrix)
        max_sharpe_weights = ef.max_sharpe(self.risk_free_rate())
        clean_weights = ef.clean_weights()

        print("\nThe weights of each stock below will"
        + Colors.bold + " maximize your"
        + " portfolio's Sharpe ratio" + Colors.end + ":")
        for stock, weight in clean_weights.items():
            print(Colors.blue + stock + Colors.end + ": " + str(round(weight, 2)))
        print()

        performance = ef.portfolio_performance(verbose=False, \
        risk_free_rate=self.risk_free_rate())
        print("Expected Annual Return:  " + str(performance[0])
            + "\nAnnual Volatility:       " + str(performance[1])
            + "\nVariance:                " + str(performance[1]**2)
            + "\nSharpe Ratio:            " + str(performance[2]) + "\n")
        
    def optimize_pf_min_volatility(self):
        stock_list = self.get_stock_list()
        data = web.DataReader(stock_list, data_source="yahoo", \
        start=minus_ten_years())['Adj Close']
        returns = data.pct_change()
        expected_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252

        ef = EfficientFrontier(expected_returns, cov_matrix)
        min_vol_weights = ef.min_volatility()
        clean_weights = ef.clean_weights()

        print("\nThe weights of each stock below will"
        + Colors.bold + " minimize your"
        + " portfolio's volatility" + Colors.end + ":")
        for stock, weight in clean_weights.items():
            print(Colors.blue + stock + Colors.end + ": " + str(round(weight, 2)))
        print()

        performance = ef.portfolio_performance(verbose=False, \
        risk_free_rate=self.risk_free_rate())
        print("Expected Annual Return:  " + str(performance[0])
            + "\nAnnual Volatility:       " + str(performance[1])
            + "\nVariance:                " + str(performance[1]**2)
            + "\nSharpe Ratio:            " + str(performance[2]) + "\n")