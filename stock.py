"""
Primary module for stocks

This module contains the stock class for the stock portfolio engine.

Daisy Shu
May 3rd, 2020
"""

import requests
import json
from colors import *
import time
from datetime import date
import pandas_datareader as pdr
import pandas_datareader.data as web
import numpy as np

class InexistentStock(Exception):
    """
    Raised when the stock entered does not exist.
    """
    pass

def minus_five_years():
    """
    Calculates the exact date five years ago, where month and day
    of the current date are unchanged.

    Returns:
        date        string; formatted yyyy-mm-dd where yyyy is five
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
        date        string; formatted yyyy-mm-dd where yyyy is ten
                    years before the current year
    """
    today = str(date.today())
    year = int(today[:4])
    year -= 10
    return str(year)+today[4:]

def get_gov_bond_rate():
    """
    Fetches stock statistics, and returns 10-year government treasury bond rate.

    Returns:
        price       float
    """
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
    params = {"region": "US", "symbol": "^TNX"}
    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
        }
    response = requests.request(
                                "GET", url,
                                headers=headers, params=params
                                )
    text = response.text
    json_text = json.loads(text)
    price = json_text["price"]["regularMarketPrice"]["raw"]
    return float(price/100)

class Stock():
    """
    Fetches the stock response from Yahoo Finance! API, and parses the data.

    Args:
        symbol      string; ticker symbol of the stock interested
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def get_short_name(self, json):
        """
        Fetches stock statistics, and returns short name of stock interested.
        If short name does not exist, returns "N/A".

        Args:
            json            json string
        Returns:
            short_name      string
        """
        try:
            short_name = json["price"]["shortName"]
            short_name = short_name.strip()
        except:
            short_name = "N/A"

        return short_name
    
    def get_long_name(self, json):
        """
        Fetches stock statistics, and returns long name of stock interested.
        If long name does not exist, returns "N/A".

        Args:
            json            json string
        Returns:
            long_name       string
        """
        try:
            long_name = json["price"]["longName"]
            long_name = long_name.strip()
        except:
            long_name = "N/A"

        return long_name

    def fetch_stock_summary(self):
        """
        Calls GET response for stock interested using Yahoo! Finance API from
        Rapid API, and fetches stock summary statistics.
        
        Summary statistics for stock interested include:
            -Short name
            -Current price
            -Previous closing price
            -Market cap
            -Beta (5Y monthly)
            -PE ratio
            -EPS
        If specific summary statistic does not exist for stock interested,
        then N/A.

        From stock summary statistics, computes difference and percent change
        between current price and previous closing price of stock interested.
        If difference is positive, string is green, red otherwise.
        
        Prints stock summary statistics.

        Returns:
            summary             string
        Raises:
            InexistentStock     exception when stock entered does not exist
        """
        try:
            url_summary = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
            params_summary = {"region": "US", "symbol": self.symbol}
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
        
            try:
                price = json_text["price"]["regularMarketPrice"]["fmt"]
                price = price.strip()
            except:
                price = "N/A"
            try:
                close = json_text["summaryDetail"]["previousClose"]["fmt"]
                close = close.strip()
            except:
                close = "N/A"
            try:
                market_cap = json_text["price"]["marketCap"]["fmt"]
                market_cap = market_cap.strip()
            except:
                market_cap = "N/A"
            try:
                beta_5Y = json_text["summaryDetail"]["beta"]["fmt"]
                beta_5Y = beta_5Y.strip()
            except:
                beta_5Y = "N/A"
            try:
                pe_ratio = json_text["summaryDetail"]["trailingPE"]["fmt"]
                pe_ratio = pe_ratio.strip()
            except:
                pe_ratio = "N/A"
            try:
                eps = json_text["summaryDetail"]["trailingEps"]["fmt"]
                eps = eps.strip()
            except:
                eps = "N/A"
                
            try:
                replace_price = price.replace(",", "")
                curr_price = float(replace_price)
                replace_price = close.replace(",", "")
                prev_close = float(replace_price)
                difference = curr_price - prev_close
                percent_change = str("%.2f"% abs(difference*100./prev_close))
                + "%"
                if difference > 0.:
                    diff_of_price = Colors.green + "+"
                    + str("%.2f"% difference) + " (+"+percent_change+")"
                    + Colors.end
                elif difference < 0.:
                    diff_of_price = Colors.red
                    + str("%.2f"% difference) + " (-"+percent_change+")"
                    + Colors.end
                else:
                    diff_of_price = Colors.black + "+"
                    + str("%.2f"% difference) + " (+"+percent_change+")"
                    + Colors.end
            except:
                diff_of_price = ""

            if (self.get_long_name(json_text) == "N/A"):
                name = self.get_short_name(json_text)
            else:
                name = self.get_long_name(json_text)

            start_time = time.time()
            print ("\n" + Colors.bold + name + " ("+self.symbol+")"
                    + Colors.end + "\n"
                    + Colors.bold + price + Colors.end + "  "
                    + diff_of_price + "\n\n"
                    + Colors.blue + "Current Price:     " + Colors.end
                    + price + "\n"
                    + Colors.blue + "Previous Close:    " + Colors.end
                    + close + "\n"
                    + Colors.blue + "Market Cap:        " + Colors.end
                    + market_cap + "\n"
                    + Colors.blue + "Beta (5Y Monthly): " + Colors.end
                    + beta_5Y + "\n"
                    + Colors.blue + "PE Ratio (TTM):    " + Colors.end
                    + pe_ratio + "\n"
                    + Colors.blue + "EPS (TTM):         " + Colors.end
                    + eps + "\n"
                    )
            print("--- %s seconds ---" % (time.time() - start_time))
        except:
            raise InexistentStock

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

    def fetch_stock_profile(self):
        """
        Calls GET response for stock interested using Yahoo! Finance API from
        Rapid API, and fetches stock summary.
        
        Profile for stock interested include:
            -Short name
            -Address
            -City
            -State
            -Zipcode
            -Country
            -Phone
            -Website
            -Sector
            -Industry
            -Number of full-time employees
            -Description of company
        If specific profile statistic does not exist for stock interested, then N/A.
        
        Prints the stock profile.

        Returns:
            profile     string
        Raises:
            InexistentStock     exception when stock entered does not exist
        """
        try:
            url_profile = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"
            params_profile = {"region": "US", "symbol": self.symbol}
            headers = {
                'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
                'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
                }
            response = requests.request(
                                        "GET", url_profile,
                                        headers=headers, params=params_profile
                                        )
            text = response.text
            json_text = json.loads(text)

            try:
                address = json_text["assetProfile"]["address1"]
                address = address.strip()
            except:
                address = ""
            try:
                city = json_text["assetProfile"]["city"]
                city = city.strip()
            except:
                city = ""
            try:
                state = json_text["assetProfile"]["state"]
                state = state.strip()
            except:
                state = ""
            try:
                zipCode = json_text["assetProfile"]["zip"]
                zipCode = zipCode.strip()
            except:
                zipCode = ""
            try:
                country = json_text["assetProfile"]["country"]
                country = country.strip()
            except:
                country = ""
            try:
                phone = json_text["assetProfile"]["phone"]
                phone = self.phone_number_converter(phone)
            except:
                phone = "N/A"
            try:
                website = json_text["assetProfile"]["website"]
                website = website.strip()
            except:
                website = "N/A"
            try:
                sector = json_text["assetProfile"]["sector"]
                sector = sector.strip()
            except:
                sector = "N/A"
            try:
                industry = json_text["assetProfile"]["industry"]
                industry = industry.strip()
            except:
                industry = "N/A"
            try:
                employees = json_text["assetProfile"]["fullTimeEmployees"]
                employees = self.split_number(str(employees), [])
            except:
                employees = "N/A"
            try:
                description = json_text["assetProfile"]["longBusinessSummary"]
                description = description.strip()
            except:
                description = "N/A"
                
            if (self.get_long_name(json_text) == "N/A"):
                name = self.get_short_name(json_text)
            else:
                name = self.get_long_name(json_text)

            start_time = time.time()
            if (address == "" and city == "" and state == ""
                and country == ""):
                print ("\n" + Colors.bold + name + " ("+self.symbol+")"
                        + Colors.end + "\n"
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
                        + Colors.end + "\n"
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
            print("--- %s seconds ---" % (time.time() - start_time))
        except:
            raise InexistentStock

    def fetch_stock_historical_data(self):
        """
        Fetches stock historical data between five years ago and current
        date from pandas' DataReader.

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