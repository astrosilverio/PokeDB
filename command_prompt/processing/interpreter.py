#!/usr/bin/env python3

########################################################
###### Interpret the command from the interactive ######
###### prompt                                     ######
########################################################
from .pokeCommands import Commands, RunIt

POKE_COMMANDS = {'help': 'helpPlease',
                 'exit': 'exitConsole',
                 'list tables': 'listTables',
                 'list databases': 'listDatabases',
                 'list users': 'listUsers'
                }

class Interpret:
    def __init__(self, command):
        self.command = command

    def runCommand(self, command):
        C = Commands()
        if POKE_COMMANDS.get(self.command):
            result = getattr(C, POKE_COMMANDS.get(command))()
        else:
            command = command.split()
        print(result)
