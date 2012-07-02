#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from lai import Client, Database, Document

client = Client(Database())
filename = '/home/xleo/src/tools12/trunk/scripts/lai/data'

with codecs.open(filename, 'r', encoding='latin1') as file:
    lines = file.readlines()
    for line in lines[1772:]:
        if line != '':
            #data = line.rsplit('#')[0].strip()
            doc = Document(line.strip())
            doc.set_keys(line)
            client.save(doc)

