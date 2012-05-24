# -*- coding: utf-8 -*-

from data import Data


class Document:

    def __init__(self, data, id=None, tid=None, sid=None, synched=True, keys=None):
        self.data = Data(data)
        self.id = id
        self.tid = tid
        self.sid = sid
        self.synched = synched
        self.keys = keys


if __name__ == '__main__':
    doc = Document('{"x": 0, "y": 1}')
    print doc.data.dumps()
