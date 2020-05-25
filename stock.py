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

class InexistentStock(Exception):
    """
    Raised when the stock entered does not exist.
    """
    pass

class Stock:
    """
    Fetches the stock response from Yahoo Finance! API, and parses the data.

    Inputs:
        symbol      string; ticker symbol of the stock interested
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def getShortName(self, json):
        """
        Fetches stock statistics, and returns short name of stock interested. If short
        name does not exist, returns "N/A".

        Output:
            shortName       string
        """
        try:
            shortName = json["price"]["shortName"]
            shortName = shortName.strip()
        except:
            shortName = "N/A"

        return shortName
    
    def getLongName(self, json):
        """
        Fetches stock statistics, and returns long name of stock interested. If long
        name does not exist, returns "N/A".

        Output:
            longName        string
        """
        try:
            longName = json["price"]["longName"]
            longName = longName.strip()
        except:
            longName = "N/A"

        return longName

    def fetchStockSummary(self):
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
        If specific summary statistic does not exist for stock interested, then N/A.

        From stock summary statistics, computes difference and percent change between
        current price and previous closing price of stock interested. If difference is
        positive, string is green, red otherwise.
        
        Prints stock summary statistics.

        Output:
            summaryStatistics       string

        """
        try:
            urlSummary = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"
            paramsSummary = {"region": "US", "symbol": self.symbol}
            headers = {
                'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
                'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
                }
            response = requests.request("GET", urlSummary, headers=headers, params=paramsSummary)
            text = response.text
            jsonText = json.loads(text)
        
            try:
                currentPrice = jsonText["price"]["regularMarketPrice"]["fmt"]
                currentPrice = currentPrice.strip()
            except:
                currentPrice = "N/A"
            try:
                previousClose = jsonText["summaryDetail"]["previousClose"]["fmt"]
                previousClose = previousClose.strip()
            except:
                previousClose = "N/A"
            try:
                marketCap = jsonText["price"]["marketCap"]["fmt"]
                marketCap = marketCap.strip()
            except:
                marketCap = "N/A"
            try:
                beta5Y = jsonText["summaryDetail"]["beta"]["fmt"]
                beta5Y = beta5Y.strip()
            except:
                beta5Y = "N/A"
            try:
                peRatio = jsonText["summaryDetail"]["trailingPE"]["fmt"]
                peRatio = peRatio.strip()
            except:
                peRatio = "N/A"
            try:
                eps = jsonText["summaryDetail"]["trailingEps"]["fmt"]
                eps = eps.strip()
            except:
                eps = "N/A"
                
            try:
                replacePrice = currentPrice.replace(",", "")
                currPrice = float(replacePrice)
                replaceClose = previousClose.replace(",", "")
                prevClose = float(replaceClose)
                difference = currPrice - prevClose
                percentChange = str("%.2f"% abs(difference*100./prevClose)) + "%"
                if difference > 0.:
                    differenceOfPrice = Colors.green + "+" + str("%.2f"% difference) + " (+"+percentChange+")" + Colors.end
                elif difference < 0.:
                    differenceOfPrice = Colors.red + str("%.2f"% difference) + " (-"+percentChange+")" + Colors.end
                else:
                    differenceOfPrice = Colors.black + "+" + str("%.2f"% difference) + " (+"+percentChange+")" + Colors.end
            except:
                differenceOfPrice = ""

            if (self.getLongName(jsonText) == "N/A"):
                name = self.getShortName(jsonText)
            else:
                name = self.getLongName(jsonText)

            start_time = time.time()
            print ("\n" + Colors.bold + name + " ("+self.symbol+")" + Colors.end + "\n" +
                    Colors.bold + currentPrice + Colors.end + "  " + differenceOfPrice + "\n\n" +
                    Colors.blue + "Current Price:     " + Colors.end + currentPrice + "\n" +
                    Colors.blue + "Previous Close:    " + Colors.end + previousClose + "\n" +
                    Colors.blue + "Market Cap:        " + Colors.end + marketCap + "\n" +
                    Colors.blue + "Beta (5Y Monthly): " + Colors.end + beta5Y + "\n" +
                    Colors.blue + "PE Ratio (TTM):    " + Colors.end + peRatio + "\n" +
                    Colors.blue + "EPS (TTM):         " + Colors.end + eps + "\n"
                    )
            print("--- %s seconds ---" % (time.time() - start_time))
        except:
            raise InexistentStock

    def phoneNumberConverter(self, number):
        """
        Converts a valid US 10-digit number to the format (xxx) xxx-xxxx.
        Returns the original number otherwise.

        Output:
            number      string
        """
        number = number.strip()
        num = number.replace("-", "")
        if (len(num) == 10):
            number = "("+num[:3]+") "+num[3:6]+"-"+num[6:]
            return number
        else:
            return number

    def splitNumber(self, number, lst):
      """
      Splits any number over 3 digits with commas for every thousandths place.

      Output:
          number    string
      """
      number = number.strip()
      if (len(number) == 0):
        return ",".join(lst[::-1])
      elif (len(number) > 0 and len(number) <= 3):
        lst.append(str(number))
        return self.splitNumber("", lst)
      else:
        lst.append(str(number[(len(number)-3):]))
        return self.splitNumber(str(number[:(len(number)-3)]), lst)

    def fetchStockProfile(self):
        """
        Calls GET response for stock interested using Yahoo! Finance API from
        Rapid API, and fetches stock summary.
        
        Summary for stock interested include:
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
        If specific summary does not exist for stock interested, then N/A.
        
        Prints stock summary statistics.

        Output:
            summary     string
        """
        try:
            urlStats = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"
            queryStringSum = {"region": "US", "symbol": self.symbol}
            headers = {
                'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
                'x-rapidapi-key': "90e7e1604dmsh5cac8815cc6907ep11256ejsnc832e71018a2"
                }
            response = requests.request("GET", urlStats, headers=headers, params=queryStringSum)
            text = response.text
            jsonText = json.loads(text)

            try:
                address = jsonText["assetProfile"]["address1"]
                address = address.strip()
            except:
                address = ""
            try:
                city = jsonText["assetProfile"]["city"]
                city = city.strip()
            except:
                city = ""
            try:
                state = jsonText["assetProfile"]["state"]
                state = state.strip()
            except:
                state = ""
            try:
                zipCode = jsonText["assetProfile"]["zip"]
                zipCode = zipCode.strip()
            except:
                zipCode = ""
            try:
                country = jsonText["assetProfile"]["country"]
                country = country.strip()
            except:
                country = ""
            try:
                phone = jsonText["assetProfile"]["phone"]
                phone = self.phoneNumberConverter(phone)
            except:
                phone = "N/A"
            try:
                website = jsonText["assetProfile"]["website"]
                website = website.strip()
            except:
                website = "N/A"
            try:
                sector = jsonText["assetProfile"]["sector"]
                sector = sector.strip()
            except:
                sector = "N/A"
            try:
                industry = jsonText["assetProfile"]["industry"]
                industry = industry.strip()
            except:
                industry = "N/A"
            try:
                fullTimeEmployees = jsonText["assetProfile"]["fullTimeEmployees"]
                fullTimeEmployees = self.splitNumber(str(fullTimeEmployees), [])
            except:
                fullTimeEmployees = "N/A"
            try:
                description = jsonText["assetProfile"]["longBusinessSummary"]
                description = description.strip()
            except:
                description = "N/A"
                
            if (self.getLongName(jsonText) == "N/A"):
                name = self.getShortName(jsonText)
            else:
                name = self.getLongName(jsonText)

            start_time = time.time()
            if (address == "" and city == "" and state == "" and country == ""):
                print ("\n" + Colors.bold + name + " ("+self.symbol+")" + Colors.end + "\n" +
                        Colors.blue + "Address:             " + Colors.end + "N/A" + "\n" +
                        Colors.blue + "Phone Number:        " + Colors.end + phone + "\n" +
                        Colors.blue + "Website:             " + Colors.end + website + "\n" +
                        Colors.blue + "Sector:              " + Colors.end + sector + "\n" +
                        Colors.blue + "Industry:            " + Colors.end + industry + "\n" +
                        Colors.blue + "Full-Time Employees: " + Colors.end + fullTimeEmployees + "\n" +
                        Colors.blue + "Description:         " + Colors.end + description + "\n"
                        )
            else:
                print ("\n" + Colors.bold + name + " ("+self.symbol+")" + Colors.end + "\n" +
                        Colors.blue + "Address:             " + Colors.end + address + "\n" +
                        "                     " + city + ", " + state + " " + zipCode + "\n" +
                        "                     " + country + "\n" +
                        Colors.blue + "Phone Number:        " + Colors.end + phone + "\n" +
                        Colors.blue + "Website:             " + Colors.end + website + "\n" +
                        Colors.blue + "Sector:              " + Colors.end + sector + "\n" +
                        Colors.blue + "Industry:            " + Colors.end + industry + "\n" +
                        Colors.blue + "Full-Time Employees: " + Colors.end + fullTimeEmployees + "\n" +
                        Colors.blue + "Description:         " + Colors.end + description + "\n"
                        )
            print("--- %s seconds ---" % (time.time() - start_time))
        except:
            raise InexistentStock