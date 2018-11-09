#!/usr/bin/env python3

########################################################
### Run command that is interpreted from interpreter ###
########################################################
from sys import exit
# TODO: ELIMINATE CLASSES

class Commands:
    def __init__(self):
        pass

    def exitConsole(self):
        exit()

    def helpPlease(self):
        return "HELP ME!!!"

    def listDatabases(self):
        return "DATABSESSSSSS"

    def listTables(self):
        return "TABLES HERE"

    def listUsers(self):
        return "USERS!"

    def startSQL(self):
        return "Now in SQL mode"

class SQLStatements:
    def __init__(self):
        pass

    def select(self):
        # 
        return "I SELECTED THIS"

    def fromTable(self):
        return "FROM THIS TABLE"
