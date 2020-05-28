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
        ticker_symbol]       "remove" (depending on which one is called) and the
                            ticker symbol that follows
    Raises:
        Empty               raised when command inputted is empty
        Malformed           raised when command is malformed; in other words, raised
                            when command is not "view", "add", "remove", "portfolio",
                            "help", or "quit", and/or, there are more letters/words
                            that follow commands "portfolio", "help", or "quit"
    """
    trim_str = input.strip()
    lowercase_str = trim_str.lower()
    if lowercase_str == "":
        raise Empty
    else:
        list_of_words = lowercase_str.split(" ")
        remove_empty = [x for x in list_of_words[:] if x != '']
        if len(remove_empty) == 0:
            raise Empty
        else:
            command = remove_empty[0]
            if len(remove_empty) > 1:
                ticker_symbol = remove_empty[1]
                category = remove_empty[2:]
                if ((command == "view" or command == "add" or command == "remove")
                and (len(category) == 0)):
                    return [command, capitalize(ticker_symbol)]
                elif (command == "view" and len(category) == 1):
                    second_command = category[0]
                    if (second_command == "profile" or second_command == "statistics" or second_command == "chart"):
                        return [command, capitalize(ticker_symbol), category[0]]
                    else:
                        raise Malformed
                elif (command == "view" and len(category) == 2):
                    second_command = category[0]
                    third_command = category[1]
                    if (second_command == "historical" and third_command == "data"):
                        return [command, capitalize(ticker_symbol), second_command, third_command]
                    else:
                        raise Malformed
                else:
                    raise Malformed
            elif (len(remove_empty) == 1):
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