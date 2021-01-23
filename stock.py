"""
Primary module for stocks

This module contains the stock class for the stock portfolio engine.

Daisy Shu
May 3rd, 2020
"""

import requests
import json
from colors import *
from datetime import date
import pandas_datareader.data as web
import numpy as np
import yfinance as yf
from bs4 import BeautifulSoup

class Stock():
    """
    Fetches the stock response from Yahoo Finance! API using yfinance Python
    library, and parses the data.

    Args:
        symbol      string; ticker symbol of the stock interested
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def get_short_name(self, json):
        """
        Fetches and returns short name of stock interested given json string.
        If short name does not exist, returns "N/A".

        Args:
            json            json string
        Returns:
            short_name      string
        """
        try:
            short_name = json["shortName"].strip()
        except:
            short_name = "N/A"

        return short_name
    
    def get_long_name(self, json):
        """
        Fetches and returns long name of stock interested given json string.
        If long name does not exist, returns "N/A".

        Args:
            json            json string
        Returns:
            long_name       string
        """
        try:
            long_name = json["longName"].strip()
        except:
            long_name = "N/A"

        return long_name

    def get_summary(self):
        """
        Web scrapes stock summary for stock interested from Yahoo! Finance
        page using Beautiful Soup Python package, and returns the stock
        summary.

        Returns:
            price,              string tuple
            market_cap
        Raises:
            InexistentStock     exception when stock entered does not exist
        """
        try:
            page = requests.get("https://finance.yahoo.com/quote/" + self.symbol)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                price = soup.select_one("div span[data-reactid='50']").text.strip()
            except:
                price = "N/A"
            try:
                market_cap = soup.select_one("td[data-test='MARKET_CAP-value']").text.strip()
            except:
                market_cap = "N/A"

            return str(price), str(market_cap)
        except:
            raise InexistentStock

    def fetch_stock_summary(self):
        """
        Combines stock information fetched from yfinance Python library and
        stock summary web scraped from Yahoo! Finance page for a given
        stock, and prints the stock summary.
        
        Summary statistics for stock interested include:
            -Name of Company
            -Current Price (+/- Percent Change)
            -Previous Closing Price
            -Market Opening Price
            -Daily High
            -Daily Low
            -52 Week High
            -52 Week Low
            -Daily Volume
            -Average Volume
            -Market Cap
            -Beta (5Y Monthly)
            -PE Ratio (TTM)
            -EPS (TTM)
            -Dividend Yield
        If specific summary statistic does not exist for stock interested,
        then N/A.

        From stock summary statistics, computes difference and percent change
        between current price and previous closing price of stock interested.
        If difference is positive, difference string is green, red otherwise.

        Returns:
            summary             string
        Raises:
            InexistentStock     exception when stock entered does not exist
        """
        try:
            stock = yf.Ticker(self.symbol)
            json_text = stock.info

            try:
                close = str(round(json_text["previousClose"], 2)).strip()
            except:
                close = "N/A"
            try:
                open = str(round(json_text["regularMarketOpen"], 2)).strip()
            except:
                open = "N/A"
            try:
                high = str(round(json_text["regularMarketDayHigh"], 2)).strip()
            except:
                high = "N/A"
            try:
                low = str(round(json_text["regularMarketDayLow"], 2)).strip()
            except:
                low = "N/A"
            try:
                fifty_two_week_high = str(round(json_text["fiftyTwoWeekHigh"], 2)).strip()
            except:
                fifty_two_week_high = "N/A"
            try:
                fifty_two_week_low = str(round(json_text["fiftyTwoWeekLow"], 2)).strip()
            except:
                fifty_two_week_low = "N/A"
            try:
                volume = str(round(json_text["volume"], 2))
                volume = self.split_number(volume, [])
            except:
                volume = "N/A"
            try:
                avg_volume = str(round(json_text["averageVolume"], 2))
                avg_volume = self.split_number(avg_volume, [])
            except:
                avg_volume = "N/A"
            try:
                beta_5Y = str(round(json_text["beta"], 2)).strip()
            except:
                beta_5Y = "N/A"
            try:
                pe_ratio = str(round(json_text["trailingPE"], 2)).strip()
            except:
                pe_ratio = "N/A"
            try:
                eps = str(round(json_text["trailingEps"], 2)).strip()
            except:
                eps = "N/A"
            try:
                div_rate = str(round(json_text["dividendRate"], 2)).strip()
            except:
                div_rate = "N/A"
            try:
                div_yield = "("+str(round(json_text["dividendYield"]*100, 2)).strip()+"%)"
            except:
                div_yield = "N/A"

            price, market_cap = self.get_summary()
                
            try:
                curr_price = float(price.replace(",", ""))
                prev_close = float(close.replace(",", ""))
                difference = curr_price - prev_close
                percent_change = str("%.2f"% abs(difference*100./prev_close)) \
                + "%"
                if difference > 0.:
                    diff_of_price = Colors.green + "+" \
                    + str("%.2f"% difference) + " (+"+percent_change+")" \
                    + Colors.end
                elif difference < 0.:
                    diff_of_price = Colors.red \
                    + str("%.2f"% difference) + " (-"+percent_change+")" \
                    + Colors.end
                else:
                    diff_of_price = Colors.black + "+" \
                    + str("%.2f"% difference) + " (+"+percent_change+")" \
                    + Colors.end
            except:
                diff_of_price = ""

            if (self.get_long_name(json_text) == "N/A"):
                name = self.get_short_name(json_text)
            else:
                name = self.get_long_name(json_text)

            print ("\n" + Colors.bold + name + " ("+self.symbol+")"
                    + Colors.end + "\n"
                    + Colors.bold + price + Colors.end + "  "
                    + diff_of_price + "\n\n"
                    + Colors.blue + "Previous Close: " + Colors.end
                    + close + "\n"
                    + Colors.blue + "Open:           " + Colors.end
                    + open + "\n"
                    + Colors.blue + "High:           " + Colors.end
                    + high + "\n"
                    + Colors.blue + "Low:            " + Colors.end
                    + low + "\n"
                    + Colors.blue + "52 Week High:   " + Colors.end
                    + fifty_two_week_high + "\n"
                    + Colors.blue + "52 Week Low:    " + Colors.end
                    + fifty_two_week_low + "\n"
                    + Colors.blue + "Today's Volume: " + Colors.end
                    + volume + "\n"
                    + Colors.blue + "Average Volume: " + Colors.end
                    + avg_volume + "\n"
                    + Colors.blue + "Market Cap:     " + Colors.end
                    + market_cap + "\n"
                    + Colors.blue + "Beta:           " + Colors.end
                    + beta_5Y + "\n"
                    + Colors.blue + "P/E Ratio:      " + Colors.end
                    + pe_ratio + "\n"
                    + Colors.blue + "EPS:            " + Colors.end
                    + eps + "\n"
                    + Colors.blue + "Div/Yield:      " + Colors.end
                    + div_rate + " " + div_yield + "\n")
        except:
            raise InexistentStock

    def fetch_stock_profile(self):
        """
        Fetches stock information from yfinance Python library for a given
        stock, and prints the stock profile.
        
        Profile for stock interested include:
            -Name of Company
            -Address
            -City
            -State
            -Zipcode
            -Country
            -Phone
            -Website
            -Sector
            -Industry
            -Number of Full-Time Employees
            -Description of Company
        If specific profile statistic does not exist for stock interested, then N/A.

        Returns:
            profile             string
        Raises:
            InexistentStock     exception when stock entered does not exist
        """
        try:
            stock = yf.Ticker(self.symbol)
            json_text = stock.info

            try:
                address = json_text["address1"].strip()
            except:
                address = ""
            try:
                city = json_text["city"].strip()
            except:
                city = ""
            try:
                state = json_text["state"].strip()
            except:
                state = ""
            try:
                zipCode = json_text["zip"].strip()
            except:
                zipCode = ""
            try:
                country = json_text["country"].strip()
            except:
                country = ""
            try:
                phone = json_text["phone"]
                phone = self.phone_number_converter(phone)
            except:
                phone = "N/A"
            try:
                website = json_text["website"].strip()
            except:
                website = "N/A"
            try:
                sector = json_text["sector"].strip()
            except:
                sector = "N/A"
            try:
                industry = json_text["industry"].strip()
            except:
                industry = "N/A"
            try:
                employees = json_text["fullTimeEmployees"]
                employees = self.split_number(str(employees), [])
            except:
                employees = "N/A"
            try:
                description = json_text["longBusinessSummary"].strip()
            except:
                description = "N/A"
                
            if (self.get_long_name(json_text) == "N/A"):
                name = self.get_short_name(json_text)
            else:
                name = self.get_long_name(json_text)

            if (address == "" and city == "" and state == "" \
                and country == ""):
                print ("\n" + Colors.bold + name + " ("+self.symbol+")"
                        + " Profile" + Colors.end + "\n"
                        + Colors.blue + "Address:             " + Colors.end
                        + "N/A" + "\n"
                        + Colors.blue + "Phone Number:        " + Colors.end
                        + phone + "\n"
                        + Colors.blue + "Website:             " + Colors.end
                        + website + "\n"
                        + Colors.blue + "Sector:              " + Colors.end
                        + sector + "\n"
                        + Colors.blue + "Industry:            " + Colors.end
                        + industry + "\n"
                        + Colors.blue + "Full-Time Employees: " + Colors.end
                        + employees + "\n"
                        + Colors.blue + "Description:         " + Colors.end
                        + description + "\n")
            else:
                print ("\n" + Colors.bold + name + " ("+self.symbol+")"
                        + " Profile" + Colors.end + "\n"
                        + Colors.blue + "Address:             " + Colors.end
                        + address + "\n"
                        + "                     " + city + ", " + state + " "
                        + zipCode + "\n"
                        + "                     " + country + "\n"
                        + Colors.blue + "Phone Number:        " + Colors.end
                        + phone + "\n"
                        + Colors.blue + "Website:             " + Colors.end
                        + website + "\n"
                        + Colors.blue + "Sector:              " + Colors.end
                        + sector + "\n"
                        + Colors.blue + "Industry:            " + Colors.end
                        + industry + "\n"
                        + Colors.blue + "Full-Time Employees: " + Colors.end
                        + employees + "\n"
                        + Colors.blue + "Description:         " + Colors.end
                        + description + "\n")
        except:
            raise InexistentStock

    def get_statistics(self):
        """
        Web scrapes stock statistics for stock interested from Yahoo! Finance
        page using Beautiful Soup Python package, and returns the stock
        statistics.

        Returns:
            revenue,                string tuple
            revenue_per_share,
            gross_profit,
            operating_margin,
            return_on_assets,
            return_on_equity
        Raises:
            InexistentStock         exception when stock entered does not
                                    exist
        """
        try:
            page = requests.get("https://finance.yahoo.com/quote/" + self.symbol + "/key-statistics")
            soup = BeautifulSoup(page.content, 'html.parser')
            div = soup.find("div", {"id": "app"})
            try:
                revenue = div.select_one("#Col1-0-KeyStatistics-Proxy > section > div.Mstart\\(a\\).Mend\\(a\\) > div.Fl\\(start\\).W\\(50\\%\\).smartphone_W\\(100\\%\\) > div > div:nth-child(4) > div > div > table > tbody > tr.Bxz\\(bb\\).H\\(36px\\).BdY.Bdc\\(\\$seperatorColor\\) > td.Fw\\(500\\).Ta\\(end\\).Pstart\\(10px\\).Miw\\(60px\\)").text.strip()
            except:
                revenue = "N/A"
            try:
                revenue_per_share = div.select_one("#Col1-0-KeyStatistics-Proxy > section > div.Mstart\\(a\\).Mend\\(a\\) > div.Fl\\(start\\).W\\(50\\%\\).smartphone_W\\(100\\%\\) > div > div:nth-child(4) > div > div > table > tbody > tr:nth-child(2) > td.Fw\\(500\\).Ta\\(end\\).Pstart\\(10px\\).Miw\\(60px\\)").text.strip()
            except:
                revenue_per_share = "N/A"
            try:
                gross_profit = div.select_one("#Col1-0-KeyStatistics-Proxy > section > div.Mstart\\(a\\).Mend\\(a\\) > div.Fl\\(start\\).W\\(50\\%\\).smartphone_W\\(100\\%\\) > div > div:nth-child(4) > div > div > table > tbody > tr:nth-child(4) > td.Fw\\(500\\).Ta\\(end\\).Pstart\\(10px\\).Miw\\(60px\\)").text.strip()
            except:
                gross_profit = "N/A"
            try:
                operating_margin = div.select_one("#Col1-0-KeyStatistics-Proxy > section > div.Mstart\\(a\\).Mend\\(a\\) > div.Fl\\(start\\).W\\(50\\%\\).smartphone_W\\(100\\%\\) > div > div:nth-child(2) > div > div > table > tbody > tr.Bxz\\(bb\\).H\\(36px\\).BdB.Bdbc\\(\\$seperatorColor\\) > td.Fw\\(500\\).Ta\\(end\\).Pstart\\(10px\\).Miw\\(60px\\)").text.strip()
            except:
                operating_margin = "N/A"
            try:
                return_on_assets = div.select_one("#Col1-0-KeyStatistics-Proxy > section > div.Mstart\\(a\\).Mend\\(a\\) > div.Fl\\(start\\).W\\(50\\%\\).smartphone_W\\(100\\%\\) > div > div:nth-child(3) > div > div > table > tbody > tr.Bxz\\(bb\\).H\\(36px\\).BdY.Bdc\\(\\$seperatorColor\\) > td.Fw\\(500\\).Ta\\(end\\).Pstart\\(10px\\).Miw\\(60px\\)").text.strip()
            except:
                return_on_assets = "N/A"
            try:
                return_on_equity = div.select_one("#Col1-0-KeyStatistics-Proxy > section > div.Mstart\\(a\\).Mend\\(a\\) > div.Fl\\(start\\).W\\(50\\%\\).smartphone_W\\(100\\%\\) > div > div:nth-child(3) > div > div > table > tbody > tr.Bxz\\(bb\\).H\\(36px\\).BdB.Bdbc\\(\\$seperatorColor\\) > td.Fw\\(500\\).Ta\\(end\\).Pstart\\(10px\\).Miw\\(60px\\)").text.strip()
            except:
                return_on_equity = "N/A"
            return str(revenue), str(revenue_per_share), str(gross_profit), \
            str(operating_margin), str(return_on_assets), \
            str(return_on_equity)
        except:
            raise InexistentStock

    def fetch_stock_statistics(self):
        """
        Combines stock information fetched from yfinance Python library and
        stock statistics web scraped from Yahoo! Finance page for a given
        stock, and prints the stock statistics.
        
        Statistics for stock interested include:
            -Name of Company
            -52-Week Low
            -52-Week High
            -52-Week Change
            -Shares Outstanding
            -Revenue (TTM)
            -Revenue Per Share (TTM)
            -Gross Profit (TTM)
            -Profit Margin
            -Operating Margin (TTM)
            -Return on Assets (TTM)
            -Return on Equity (TTM)
            -Dividend Rate
            -Short Ratio
        If specific statistic does not exist for stock interested, then N/A.

        Returns:
            statistics          string
        Raises:
            InexistentStock     exception when stock entered does not exist
        """
        try:
            stock = yf.Ticker(self.symbol)
            json_text = stock.info

            try:
                fifty_two_week_low = str(round(json_text["fiftyTwoWeekLow"], 2)).strip()
            except:
                fifty_two_week_low = "N/A"
            try:
                fifty_two_week_high = str(round(json_text["fiftyTwoWeekHigh"], 2)).strip()
            except:
                fifty_two_week_high = "N/A"
            try:
                fifty_two_week_change = str(round(json_text["52WeekChange"]*100, 2)).strip() + "%"
            except:
                fifty_two_week_change = "N/A"
            try:
                shares_outstanding = self.split_number(str(round(json_text["sharesOutstanding"], 2)), []).strip()
            except:
                shares_outstanding = "N/A"
            try:
                profit_margin = str(round(json_text["profitMargins"], 2)).strip()
            except:
                profit_margin = "N/A"
            try:
                dividend_rate = str(round(json_text["dividendRate"], 2)).strip()
            except:
                dividend_rate = "N/A"
            try:
                short_ratio = str(round(json_text["shortRatio"], 2)).strip()
            except:
                short_ratio = "N/A"

            revenue, revenue_per_share, gross_profit, operating_margin, \
            return_on_assets, return_on_equity = self.get_statistics()

            if (self.get_long_name(json_text) == "N/A"):
                name = self.get_short_name(json_text)
            else:
                name = self.get_long_name(json_text)

            print ("\n" + Colors.bold + name + " ("+self.symbol+") Statistics"
                    + Colors.end + "\n"
                    + Colors.blue + "52-Week Low:        " + Colors.end
                    + fifty_two_week_low + "\n"
                    + Colors.blue + "52-Week High:       " + Colors.end
                    + fifty_two_week_high + "\n"
                    + Colors.blue + "52-Week Change:     " + Colors.end
                    + fifty_two_week_change + "\n"
                    + Colors.blue + "Shares Outstanding: " + Colors.end
                    + shares_outstanding + "\n"
                    + Colors.blue + "Revenue:            " + Colors.end
                    + revenue + "\n"
                    + Colors.blue + "Revenue Per Share:  " + Colors.end
                    + revenue_per_share + "\n"
                    + Colors.blue + "Gross Profit:       " + Colors.end
                    + gross_profit + "\n"
                    + Colors.blue + "Profit Margin:      " + Colors.end
                    + profit_margin + "\n"
                    + Colors.blue + "Operating Margin:   " + Colors.end
                    + operating_margin + "\n"
                    + Colors.blue + "Return on Assets:   " + Colors.end
                    + return_on_assets + "\n"
                    + Colors.blue + "Return on Equity:   " + Colors.end
                    + return_on_equity + "\n"
                    + Colors.blue + "Dividend Rate:      " + Colors.end
                    + dividend_rate + "\n"
                    + Colors.blue + "Short Ratio:        " + Colors.end
                    + short_ratio + "\n")
        except:
            raise InexistentStock

    def fetch_stock_historical_data(self):
        """
        Fetches stock historical data between five years ago and current
        date from Pandas' DataReader.

        Returns:
            historical_data     string; table of historical data for
                                stock interested
        """
        period1 = minus_five_years()
        period2 = str(date.today())
        print()
        print(web.get_data_yahoo(self.symbol, period1, period2))

    def stock_return_sd(self):
        """
        Calculates annualized mean return and standard deviation
        of stock interested.

        Returns:
            return_sd      string
        """
        data = web.DataReader(self.symbol, data_source="yahoo",
        start=minus_five_years())['Adj Close']
        data.sort_index(inplace=True)
        returns = data.pct_change()
        mean_return = returns.mean()
        sd_return = returns.std()
        annualized_return = round(mean_return * 252, 2)
        annualized_sd = round(sd_return * np.sqrt(252), 2)

        print(Colors.blue + "\nThe annualized mean return of stock "
            + self.symbol + " is " + str(annualized_return)
            + ", and the annualized volatility\n" + "is "
            + str(annualized_sd) + ".\n" + Colors.end)

    def split_number(self, number, lst):
        """
        Splits any number over 3 digits with commas for every thousandths place.

        Args:
            number      string
            lst         string list
        Returns:
            number      string
        """
        number = number.strip()
        if (len(number) == 0):
            return ",".join(lst[::-1])
        elif (len(number) > 0 and len(number) <= 3):
            lst.append(str(number))
            return self.split_number("", lst)
        else:
            lst.append(str(number[(len(number)-3):]))
            return self.split_number(str(number[:(len(number)-3)]), lst)

    def phone_number_converter(self, number):
        """
        Converts a valid 10-digit US number to the format (xxx) xxx-xxxx.
        Returns the original number otherwise.

        Args:
            number      int
        Returns:
            number      string in format (xxx) xxx-xxxx
        """
        number = number.strip()
        num = number.replace("-", "")
        if (len(num) == 10):
            number = "("+num[:3]+") "+num[3:6]+"-"+num[6:]
            return number
        else:
            return number

class InexistentStock(Exception):
    """
    Raised when the stock entered does not exist.
    """
    pass

class TreasuryYieldFetchError(Exception):
    """
    Raised when an error occurs when fetching yield of government treasury
    bond from Yahoo! Finance.
    """
    pass

def get_gov_bond_rate():
    """
    Web scrapes current rate (percentage) for Treasury Yield 10 Years from
    Yahoo! Finance page using Beautiful Soup Python package, and returns
    its current rate (percentage) divided by 100.

    Returns:
        price                       float
    Raises:
        TreasuryYieldFetchError     exception when an error occurs when
                                    fetching yield of government treasury
                                    bond
    """
    try:
        page = requests.get("https://finance.yahoo.com/quote/^TNX")
        soup = BeautifulSoup(page.content, 'html.parser')
        price = soup.select_one("div span[data-reactid='33']").text.strip()
        return float(price)/100.0
    except:
        raise TreasuryYieldFetchError

def minus_five_years():
    """
    Calculates the exact date five years ago, where month and day
    of the current date are unchanged.

    Returns:
        date        string; formatted YYYY-MM-DD where YYYY is five
                    years before the current year
    """
    today = str(date.today())
    year = int(today[:4])
    year -= 5
    return str(year)+today[4:]

def minus_ten_years():
    """
    Calculates the exact date ten years ago, where month and day
    of the current date are unchanged.

    Returns:
        date        string; formatted YYYY-MM-DD where YYYY is ten
                    years before the current year
    """
    today = str(date.today())
    year = int(today[:4])
    year -= 10
    return str(year)+today[4:]