#!bin/python -i

# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

import sys
import atexit
import os
import readline
import rlcompleter

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


database = Database(**config.database)
client = Client(database)

print "Python", sys.version.split('\n')[0]
print "Welcome to lai shell"
print "Autocompletion and history are enabled"
print ""
print "Lai objects:"
print "    config    (module)  from lai import config"
print "    Database  (class)   from lai import Database"
print "    Client    (class)   from lai import Client"
print "    Document  (class)   from lai import Document"
print "    database  (object)  database = Database()"
print "    client    (object)  client = Client(database)"
print ""
