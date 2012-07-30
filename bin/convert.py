#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from lai import Client, Database, Document

client = Client(Database())
filename = '/home/xleo/src/tools12/trunk/scripts/lai/data'

with codecs.open(filename, 'r', encoding='latin1') as file:
    lines = file.readlines()
    count = 0
    for line in lines[1772:]:
        if line != '':
            data = line.strip()
            doc = Document(data)
            doc = client.save(doc)
            if count % 25 == 0:
                client.sync()
            count += 1
    client.sync()

