#!/usr/bin/env python3

########################################################
###### Interpret the command from the interactive ######
###### prompt                                     ######
########################################################
from .pokeCommands import Commands, SQLStatements

POKE_COMMANDS = {'help': 'helpPlease',
                 'exit': 'exitConsole',
                 'list tables': 'listTables',
                 'list databases': 'listDatabases',
                 'list users': 'listUsers',
                 'SQL': 'startSQL'
                }
SQL_STATEMENTS = {'select': 'select',
                  'from': 'fromTable'
                 }

class Interpret:
    def __init__(self, user_input):
        self.command = user_input
        self.statement = user_input

    def runCommand(self):
        C = Commands()
        if POKE_COMMANDS.get(self.command):
            result = getattr(C, POKE_COMMANDS.get(self.command))()
            print(result)
        else:
            print("Command not defined")

    def runSQL(self):
        SQL = SQLStatements()
        split_statement = self.statement.split()
        for word in split_statement:
            if SQL_STATEMENTS.get(word):
                result = getattr(SQL, SQL_STATEMENTS.get(word))
                print(result)
