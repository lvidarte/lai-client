#!/usr/bin/env python
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

import codecs
from lai import Client, Database, Document, Data

client = Client(Database())
filename = '/tmp/docs'

with codecs.open(filename, 'r', encoding='utf8') as file:
    lines = file.readlines()
    count = 0
    for line in lines:
        tokens = line.rsplit('#', 1)
        content = tokens[0].strip()
        if len(tokens) == 2:
            description = tokens[1].strip()
        else:
            description = None
        doc = Document(Data(content, description))
        doc = client.save(doc)
        if count % 50 == 0:
            client.sync()
        count += 1
    #client.sync()

