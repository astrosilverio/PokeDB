#!/usr/bin/env python3

########################################################
###### Interpret the command from the interactive ######
###### prompt                                     ######
########################################################
from .pokeCommands import Commands, RunIt

POKE_COMMANDS = {'help': Commands.helpPlease,
                 'exit': Commands.exitConsole,
                 'list tables': Commands.listTables,
                 'list databases': Commands.listDatabases
                }

class Interpret(Commands):
    def __init__(self, command):
        self.command = command

    def runCommand(self, command):
        if POKE_COMMANDS.get(self.command):
            POKE_COMMANDS.get(self.command)
        else:
            command = command.split()
