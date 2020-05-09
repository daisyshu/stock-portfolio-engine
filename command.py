"""
Primary module for commands

This module contains the main command functions for the stock portfolio engine.

Daisy Shu
May 3rd, 2020
"""

class Empty(Exception):
   """Raised when the input command is empty."""
   pass

class Malformed(Exception):
   """Raised when the input command is malformed."""
   pass

def parse(input):
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
            rest_after_command = remove_empty[1:]
            rest_after_tick = remove_empty[2:]
            if not (command == "view" or command == "add" or command == "remove" or command == "portfolio" or command == "quit"):
                raise Malformed
            elif len(remove_empty) > 1:
                ticker_symbol = remove_empty[1]
                if (command == "view" or command == "add" or command == "remove") and (len(rest_after_tick) == 0):
                    return [command, capitalize(ticker_symbol)]
                else:
                    raise Malformed
            elif (command == "portfolio" or command == "quit") and (len(rest_after_command) == 0):
                return [command]
            else:
                raise Malformed

def capitalize(str):
    return str.upper()