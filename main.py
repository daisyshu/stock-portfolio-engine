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

def main():
    menuInstructions()
    menu()

def menuInstructions():
    print("\n*************************************************************** MAIN MENU ***************************************************************")
    print("Welcome to my stock portfolio optmization engine, where you can" +
           " view live data on any stock and customize your own stock " +
           "portfolio easily.\nThis engine will give you statistics on your " +
           "current portfolio, " + "including weights and expected returns, " +
           "so that you can make the best\ndecisions on what stocks to " +
           "include in your portfolio investment. Please choose from the" +
           " menu options below:\n")
    print( "View [ticker]   (to view any stock with a given ticker symbol [ticker])\n" +
           "Add [ticker]    (to add any stock with a given ticker symbol [ticker] to your portfolio)\n" +
           "Remove [ticker] (to remove any stock with a given ticker symbol [ticker] to your portfolio)\n" +
           "Portfolio       (to view your current portfolio)\n" +
           "Quit            (to quit the engine)\n")

def menu():
    option = input("> ")

    try:
        if parse(option)[0] == "view":
            print(parse(option)[1])
            menu()
        elif parse(option)[0] == "add":
            print(parse(option)[1])
            menu()
        elif parse(option)[0] == "remove":
            print(parse(option)[1])
            menu()
        elif parse(option)[0] == "portfolio":
            print(parse(option)[0])
            menu()
        elif parse(option)[0] == "quit":
            print("\nSorry to see you go!")
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


if __name__ == "__main__":
    main()