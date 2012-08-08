#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

