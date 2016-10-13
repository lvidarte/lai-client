# -*- coding: utf-8 -*-

# Author: Leo Vidarte <http://nerdlabs.com.ar>
#
# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['config', 'Client', 'Database', 'Document', 'Data']
from lai.client import Client
from lai.document import Document
from lai.database import Database
from lai.data import Data

prog = 'lai'
version = '0.3.4'
description = '''%s is a command line program to store notes
and keep them synchronized between multiple computers.
The idea is to keep your commands, shortcuts, snippets and
anything you want to have on hand at the console.
You can also share notes with others.''' % prog
