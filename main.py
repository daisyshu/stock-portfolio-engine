"""
This is the module with the application code.  Make sure that this module is
in a folder with the following files:

    command.py      (the primary location for command functions)
    stock.py        (the primary location for stock functions)
    portfolio.py    (the primary location for portfolio functions)
    colors.py       (the primary location for different terminal colors)

Moving any of these folders or files will prevent the engine from working
properly.

Author:         Daisy Shu
Date Created:   May 3rd, 2020 (Python 3.7.3 Version)
"""

import sys
from colors import *
from command import *
from stock import *
from portfolio import *
from help import *

def main():
    menuInstructions()
    menu()

def menuInstructions():
    print("\n************************************************** MAIN MENU"
    + " **************************************************")
    print(Colors.magenta + "Welcome to my stock portfolio optmization engine,"
        + " where you can view live data on any stock and easily customize"
        + " your own stock portfolio. This engine will give you statistics on"
        + " your current portfolio, including the expected returns and"
        + " volatility, so that you can make the best decisions on what"
        + " stocks to include in your portfolio investment. Based on the"
        + " stocks you choose, the stock portfolio engine will also provide"
        + " you information on how to achieve the optimal portfolio, or a"
        + " portfolio with the maximum possible expected returns for a given"
        + " level of risk." + Colors.end
        + "\n\nPlease choose from the menu options below:\n"
        )
    print("View   [ticker]                  "
        + "(to view any stock summary with a given ticker symbol [ticker])\n"
        + "View   [ticker] profile          "
        + "(to view any stock profile with a given ticker symbol [ticker])\n"
        + "View   [ticker] statistics       "
        + "(to view any stock statistics with a given ticker symbol"
        + " [ticker])\n"
        + "View   [ticker] historical data  "
        + "(to view any stock historial data with a given ticker symbol"
        + " [ticker])\n"
        + "View   [ticker] chart            "
        + "(to view any stock chart with a given ticker symbol [ticker])\n"
        + "Add    [ticker]                  "
        + "(to add any stock with a given ticker symbol [ticker] to your"
        + " portfolio)\n"
        + "Remove [ticker]                  "
        + "(to remove any stock with a given ticker symbol [ticker] from your"
        + " portfolio)\n"
        + "Portfolio                        "
        + "(to view your current portfolio and its data)\n"
        + "Optimize portfolio               "
        + "(to optimize your current portfolio based on different criteria)\n"
        + "Help                             "
        + "(to access the help manual)\n"
        + "Quit                             "
        + "(to quit the engine)\n\n"
        + "Examples:\n"
        + "view goog\n"
        + "view goog profile\n"
        + "add goog\n"
        + "remove goog\n"
        + "portfolio\n\n"
        + Colors.yellow + "Note: you can enter uppercase or lowercase"
        + " letters, whichever you prefer!\n" + Colors.end)

def add_weights(yes_no):
    try:
        if (yes_no.strip() == "yes"):
            weights_list = input("\nPlease enter your weights"
            + " below (separated by commas) for the following stocks in your"
            + " portfolio:\n"
            + Colors.yellow + "Note: Your weights should add to 1.\n\n"
            + Colors.end + "  "
            + list_to_string(Portfolio().get_stock_list()) + "\n> ")

            Portfolio().print_portfolio(weights_list)
        elif (yes_no.strip() == "no"):
            stock_list = Portfolio().get_stock_list()
            len_stock_list = len(stock_list)
            weights_list = ""
            for stock in stock_list:
                weights_list = weights_list + "," \
                + str(float(1/len_stock_list))
            Portfolio().print_portfolio(weights_list)
        elif (yes_no.strip() == "back"):
            print("\nYou may now choose any options from the main menu.")
        else:
            answer = input("\nPlease enter 'yes', 'no', or"
            + " 'back' if you want to go back to the main menu.\n> ")
            if answer == "back":
                print("\nYou may now choose any options from the main menu.")
            else:
                add_weights(answer)
    except WeightsMismatch:
        print(Colors.red + "The number of weights does not match"
        + " the number of stocks in your portfolio.\n" + Colors.end)
        add_weights("yes")
    except WeightsMiscalculation:
        print(Colors.red + "The total weights you entered do not add"
        + " up to 1.\n" + Colors.end)
        add_weights("yes")
    except WeightsMalformed:
        print(Colors.red + "The weights you entered were malformed. Please"
        + " make sure the numbers you enter sum to 1 and are separated by"
        + " commas.\n" + Colors.end)
        add_weights("yes")

def ask(question):
    try:
        if (question == "again"):
            question = input("\n> ")
            ask(question)
        elif (question.strip() == "back"):
            print("\nYou may now choose any options from the main menu.")
        else:
            help_manual(question)
            ask("again")
    except NoAnswer:
        print("\nI don't know how to answer that.")
        ask("again")

def menu():
    option = input("> ")

    try:
        first = parse(option)[0]
        after_command = parse(option)[1:]
        # Stock Summary
        if (first == "view" and len(after_command) == 1):
            symbol = parse(option)[1]
            Stock(symbol).fetch_stock_summary()
            menu()
        elif (first == "view" and len(after_command) == 2):
            symbol = parse(option)[1]
            second = parse(option)[2]
        # Stock Profile
            if second == "profile":
                Stock(symbol).fetch_stock_profile()
        # Stock Statistics
            if second == "statistics":
                Stock(symbol).fetch_stock_statistics()
            menu()
        # Stock Historical Data
        elif (first == "view" and len(after_command) == 3):
            symbol = parse(option)[1]
            Stock(symbol).fetch_stock_historical_data()
            Stock(symbol).stock_return_sd()
            menu()
        # Add Stock
        elif (first == "add"):
            symbol = parse(option)[1]
            portfolio = Portfolio().add_stock(symbol)
            stock_list = portfolio["Stock List"]
            print("Your stock portfolio currently contains "
            + list_to_string(stock_list) + ".\n")
            menu()
        # Remove Stock
        elif (first == "remove"):
            symbol = parse(option)[1]
            portfolio = Portfolio().remove_stock(symbol)
            stock_list = portfolio["Stock List"]
            if len(stock_list) == 0:
                print("Your stock portfolio is currently empty."
                + " Add more stocks to your portfolio!\n")
            else:
                print("Your stock portfolio currently contains "
                + list_to_string(stock_list) + ".\n")
            menu()
        # Portfolio
        elif (first == "portfolio"):
            stock_list = Portfolio().get_stock_list()
            if len(stock_list) == 0:
                print("\nYour stock portfolio is currently empty. Add more"
                + " stocks to see your portfolio data!\n")
                menu()
            elif len(stock_list) == 1:
                Portfolio().print_portfolio("1.0")
                menu()
            else:
                yes_no = input("\nWould you like to enter weights"
                + " for each stock? (enter 'yes', 'no', or 'back'"
                + " to go back to the main menu)"
                + Colors.yellow + "\nNote: if you enter 'no', your stocks will"
                + " have equally distributed weight in your portfolio."
                + Colors.end + "\n> ")
                add_weights(yes_no)
                menu()
        elif (first == "optimize"):
            stock_list = Portfolio().get_stock_list()
            if len(stock_list) == 0:
                print("\nYour stock portfolio is currently empty. Add more"
                + " stocks to see your portfolio data!\n")
                menu()
            elif len(stock_list) == 1:
                Portfolio().print_portfolio("1.0")
                menu()
            else:
                Portfolio().optimize_pf_max_sharpe()
                Portfolio().optimize_pf_min_volatility()
                menu()
        # Help
        elif (first == "help"):
            question = input("\nWhat can I help you with today? (enter"
            + " 'back' anytime to go back to the main menu)\n> ")
            ask(question)
            menu()
        # Quit
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