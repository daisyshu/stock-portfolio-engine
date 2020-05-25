"""
This is the module with the application code.  Make sure that this module is
in a folder with the following files:

    command.py      (the primary location for command functions)
    stock.py        (the primary location for stock functions)
    portfolio.py    (the primary location for portfolio functions)

Moving any of these folders or files will prevent the engine from working properly.

Author:         Daisy Shu
Date Created:   May 3rd, 2020 (Python 3 Version)
"""

import sys
from command import *
from stock import *
from portfolio import *
from colors import *

def main():
    menuInstructions()
    menu()

def menuInstructions():
    print("\n************************************************** MAIN MENU **************************************************")
    print(Colors.magenta + "Welcome to my stock portfolio optmization engine, where " +
          "you can view live data on any stock and customize your own stock " +
          "portfolio easily. This engine will give you statistics on your " +
          "current portfolio, including weights and expected returns, " +
          "so that you can make the best decisions on what stocks to " +
          "include in your portfolio investment. Please choose from the " +
          "menu options below:\n" + Colors.end)
    print("View   [ticker]                  (to view any stock summary with a given ticker symbol [ticker])\n" +
          "View   [ticker] profile          (to view any stock profile with a given ticker symbol [ticker])\n" +
          "View   [ticker] statistics       (to view any stock statistics with a given ticker symbol [ticker])\n" +
          "View   [ticker] historical data  (to view any stock historial data with a given ticker symbol [ticker])\n" +
          "View   [ticker] chart            (to view any stock chart with a given ticker symbol [ticker])\n" +
          "Add    [ticker]                  (to add any stock with a given ticker symbol [ticker] to your portfolio)\n" +
          "Remove [ticker]                  (to remove any stock with a given ticker symbol [ticker] from your portfolio)\n" +
          "Portfolio                        (to view your current portfolio and its data)\n" +
          "Help                             (to access the help manual)\n" +
          "Quit                             (to quit the engine)\n\n" +
          "Examples:\n" +
          "view goog\n" +
          "view goog profile\n" +
          "add goog\n" +
          "remove goog\n" +
          "portfolio\n\n" +
          Colors.yellow + "Note: you can enter uppercase or lowercase letters, whichever you prefer!\n" + Colors.end)

def menu():
    option = input("> ")

    try:
        first = parse(option)[0]
        afterCommand = parse(option)[1:]
        if (first == "view" and len(afterCommand) == 1):
            symbol = parse(option)[1]
            Stock(symbol).fetchStockSummary()
            menu()
        elif (first == "view" and len(afterCommand) == 2):
            symbol = parse(option)[1]
            second = parse(option)[2]
            if second == "profile":
                Stock(symbol).fetchStockProfile()
            menu()
        elif (first == "view" and len(afterCommand) == 3):
            print(parse(option)[2] + " " + parse(option)[3])
            menu()
        elif (first == "add"):
            symbol = parse(option)[1]
            portfolio = Portfolio().addStock(symbol)
            stockList = portfolio["stockList"]
            print("Your stock portfolio currently contains " + listToString(stockList) + ".\n")
            menu()
        elif (first == "remove"):
            symbol = parse(option)[1]
            portfolio = Portfolio().removeStock(symbol)
            stockList = portfolio["stockList"]
            if len(stockList) == 0:
                print("Your stock portfolio is currently empty. Add more stocks to your portfolio!\n")
            else:
                print("Your stock portfolio currently contains " + listToString(stockList) + ".\n")
            menu()
        elif (first == "portfolio"):
            Portfolio().printPortfolio()
            menu()
        elif (first == "help"):
            print(parse(option)[0])
            menu()
        elif (first == "quit"):
            print("\nSorry to see you go!\n")
            sys.exit
        else:
            menu()
    except Empty:
        print("Please enter a command.\n")
        menu()
    except Malformed:
        print("Invalid command.")
        print("You must choose one of the menu options.\n")
        menu()
    except InexistentStock:
        print("The stock you entered does not exist.")
        print("Please enter a valid stock.\n")
        menu()

if __name__ == "__main__":
    main()