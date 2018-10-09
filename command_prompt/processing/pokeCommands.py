#!/usr/bin/env python3

########################################################
### Run command that is interpreted from interpreter ###
########################################################
from sys import exit

class Commands():
    def __init__(self):
        pass

    def helpPlease(self):
        return "HELP ME!!!"

    def exitConsole(self):
        exit()

    def listTables(self):
        return "TABLES HERE"

    def listDatabases(self):
        return "DATABSESSSSSS"

    def listUsers(self):
        return "USERS!"

class RunIt(Commands):

    def runPokeCommand(self, command):
        return Commands.command
