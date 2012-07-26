#!bin/python -i

# Add auto-completion and a stored history file of commands to your Python
# interactive interpreter. Requires Python 2.0+, readline. Autocomplete is
# bound to the Esc key by default (you can change it - see readline docs).
#
# Store the file in ~/.pystartup, and set an environment variable to point
# to it:  "export PYTHONSTARTUP=/home/user/.pystartup" in bash.
#
# Note that PYTHONSTARTUP does *not* expand "~", so you have to put in the
# full path to your home directory.

import sys
import atexit
import os
import readline
import rlcompleter

from pprint import pprint as pp
from lai import config, Client, Database, Document


historyPath = os.path.expanduser("~/.pyhistory")

#readline.parse_and_bind('tab: menu-complete')
readline.parse_and_bind('tab: complete')

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

if os.path.exists(historyPath):
    readline.read_history_file(historyPath)

atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath


# lai
database = Database()
client = Client(database)

print "Python", sys.version.split('\n')[0]
print "Welcome to lai shell"
