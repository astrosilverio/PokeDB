#!/usr/bin/env python3

#########################################################
###### This is the REPL (Read-Evaluate-Print-Loop) ######
###### language shell for accessing our database   ######
#########################################################
from processing.interpreter import Interpret

def prompt():
    user_name = "Dumbledore"                #<---Make this a login based user thingy-ma-bobber get_username(login)...
    db_name = ""                            #<---Make this account for changing databases get_database(command)...
    while True:
        user_input = input("%s@%s-->" %(db_name, user_name) )
        I = Interpret(user_input)
        I.runCommand(user_input)

if __name__ == "__main__":
    prompt()
