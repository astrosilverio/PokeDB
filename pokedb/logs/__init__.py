"""
API:
`log`
"""
import os

LOGFILE = os.getenv('LOGFILE', 'poke.log')


def log(something):
    with open(LOGFILE, 'w') as logfile:
        logfile.write(something)
