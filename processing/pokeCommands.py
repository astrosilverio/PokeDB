#!/usr/bin/env python3

########################################################
### Run command that is interpreted from interpreter ###
########################################################

class Commands():
    def __init__(self):
        pass

    def helpPlease(self):
        return "HELP ME!!!"

    def exitConsole(self):
        sys.exit()

    def listTables(self):
        "TABLES HERE"

    def listDatabases(self):
        "DATABSESSSSSS"

    def listUsers(self):
        "USERS!"

class RunIt(Commands):

    def runPokeCommand(self, command):
        return Commands.command
