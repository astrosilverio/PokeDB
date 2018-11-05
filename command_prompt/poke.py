#!/usr/bin/env python3

#########################################################
###### This is the REPL (Read-Evaluate-Print-Loop) ######
###### language shell for accessing our database   ######
#########################################################
from processing.interpreter import Interpret

def prompt():
    user_name = "Dumbledore"                #<---Make this a login based user thingy-ma-bobber get_username(login)...
    db_name = ""                            #<---Make this account for changing databases get_database(command)...
    mode = "-->"
    while True:
        user_input = input("%s@%s%s " %(db_name, user_name, mode) )
        I = Interpret(user_input)
        if user_input == "SQL" and mode == "-->":
            mode = "={"
            I.runSQL()
        elif user_input == "SQL" and mode == "={":
            print("Invalid SQL statement.")
        elif mode == "={":
            I.runSQL()
        else:
            I.runCommand()

if __name__ == "__main__":
    prompt()
