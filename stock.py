import requests
import json
from colors import *

class Stock:
    """
    Fetches the stock response from Yahoo Finance! API, and parses the data.

    Inputs:
        symbol  string; ticker symbol of the stock interested
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def fetchStockStatistics(self):
        """
        Fetches stock statistics, and returns GET response for stock interested.
        """
        urlStats = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
        queryStringStats = {"region": "US", "symbol": self.symbol}
        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
            }
        response = requests.request("GET", urlStats, headers=headers, params=queryStringStats)
        text = response.text

        return json.loads(text)
        
    def fetchStockSummary(self):
        """
        Fetches stock summary, and returns GET response for stock interested.
        """
        urlSum = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
        queryStringSum = {"region":"US","symbol": self.symbol}
        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
            }
        response = requests.request("GET", urlSum, headers=headers, params=queryStringSum)
        text = response.text

        return json.loads(text)

    def getShortName(self):
        """
        Fetches stock statistics, and returns short name of stock interested. If short
        name does not exist, returns "N/A".
        Output:
            shortName   string
        """
        try:
          shortName = self.fetchStockStatistics()["price"]["shortName"]
        except:
          shortName = "N/A"

        return shortName

    def getCurrentPrice(self):
        """
        Fetches stock statistics, and returns current price of stock interested. If
        current price does not exist, returns "N/A".
        Output:
            currentPrice   string
        """
        try:
          currentPrice = self.fetchStockStatistics()["price"]["regularMarketPrice"]["fmt"]
        except:
          currentPrice = "N/A"

        return currentPrice

    def getPreviousClose(self):
        """
        Fetches stock statistics, and returns previous closing price of stock interested.
        If previous closing price does not exist, returns "N/A".
        Output:
            previousClose   string
        """
        try:
          previousClose = self.fetchStockStatistics()["summaryDetail"]["previousClose"]["fmt"]
        except:
          previousClose = "N/A"

        return previousClose

    def getMarketCap(self):
        """
        Fetches stock statistics, and returns market cap of stock interested. If market
        cap does not exist, returns "N/A".
        Output:
            marketCap   string
        """
        try:
          marketCap = self.fetchStockStatistics()["price"]["marketCap"]["fmt"]
        except:
          marketCap = "N/A"

        return marketCap

    def getBeta5Y(self):
        """
        Fetches stock statistics, and returns beta (5Y monthly) of stock interested. If
        beta does not exist, returns "N/A".
        Output:
            beta5Y   string
        """
        try:
          beta5Y = self.fetchStockStatistics()["summaryDetail"]["beta"]["fmt"]
        except:
          beta5Y = "N/A"

        return beta5Y

    def getPERatio(self):
        """
        Fetches stock statistics, and returns PE ratio of stock interested. If PE
        ratio does not exist, returns "N/A".
        Output:
            peRatio   string
        """
        try:
          peRatio = self.fetchStockStatistics()["summaryDetail"]["trailingPE"]["fmt"]
        except:
          peRatio = "N/A"

        return peRatio

    def getEPS(self):
        """
        Fetches stock statistics, and returns earnings per share (EPS) of stock
        interested. If EPS does not exist, returns "N/A".
        Output:
            eps   string
        """
        try:
          eps = self.fetchStockStatistics()["summaryDetail"]["trailingEps"]["fmt"]
        except:
          eps = "N/A"

        return eps

    def differenceOfPrice(self):
        """
        Returns difference and percent change between current price and previous
        closing price of stock interested. If difference is positive, string returned
        is green, red otherwise.
        Output:
            difference   string
        """
        currPrice = float(self.getCurrentPrice())
        previousClose = float(self.getPreviousClose())
        difference = currPrice - previousClose
        percentChange = str("%.2f"% abs(difference*100./previousClose)) + "%"
        if difference > 0.:
          return Colors.green + "+" + str("%.2f"% difference) + " (+"+percentChange+")" + Colors.end
        elif difference < 0.:
          return Colors.red + str("%.2f"% difference) + " (-"+percentChange+")" + Colors.end
        else:
          return Colors.black + "+" + str("%.2f"% difference) + " (+"+percentChange+")" + Colors.end