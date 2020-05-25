"""
Primary module for commands

This module contains the main command functions for the stock portfolio engine.

Daisy Shu
May 3rd, 2020
"""

class Empty(Exception):
   """
   Raised when the input command is empty.
   """
   pass

class Malformed(Exception):
   """
   Raised when the input command is malformed.
   """
   pass

def parse(input):
    """
    Returns string [input] parsed into a string list.

    Input:
        input               string
    Output:
        [command]           string list containing commands "portfolio" or "quit"
                            (depending on which one is called)
        [command,           string list containing commands "view", "add", or
        tickerSymbol]       "remove" (depending on which one is called) and the
                            ticker symbol that follows
    Raises:
        Empty               raised when command inputted is empty
        Malformed           raised when command is malformed; in other words, raised
                            when command is not "view", "add", "remove", "portfolio",
                            "help", or "quit", and/or, there are more letters/words
                            that follow commands "portfolio", "help", or "quit"
    """
    trimStr = input.strip()
    lowercaseStr = trimStr.lower()
    if lowercaseStr == "":
        raise Empty
    else:
        list_of_words = lowercaseStr.split(" ")
        removeEmpty = [x for x in list_of_words[:] if x != '']
        if len(removeEmpty) == 0:
            raise Empty
        else:
            command = removeEmpty[0]
            afterCommand = removeEmpty[1:]
            if len(removeEmpty) > 1:
                tickerSymbol = removeEmpty[1]
                category = removeEmpty[2:]
                if ((command == "view" or command == "add" or command == "remove")
                and (len(category) == 0)):
                    return [command, capitalize(tickerSymbol)]
                elif (command == "view" and len(category) == 1):
                    secondCommand = category[0]
                    if (secondCommand == "profile" or secondCommand == "statistics" or secondCommand == "chart"):
                        return [command, capitalize(tickerSymbol), category[0]]
                    else:
                        raise Malformed
                elif (command == "view" and len(category) == 2):
                    secondCommand = category[0]
                    thirdCommand = category[1]
                    if (secondCommand == "historical" and thirdCommand == "data"):
                        return [command, capitalize(tickerSymbol), secondCommand, thirdCommand]
                    else:
                        raise Malformed
                else:
                    raise Malformed
            elif (len(removeEmpty) == 1):
                if (command == "portfolio" or command == "help" or command == "quit"):
                    return [command]
                else:
                    raise Malformed
            else:
                raise Malformed

def capitalize(str):
    """
    Returns string [str] capitalized.

    Input:
        str             string
    Output:
        uppercase_str   string
    """

    return str.upper()