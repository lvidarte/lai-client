# -*- coding: utf-8 -*-

import json

class Data(dict):

    def __init__(self, data):
        try:
            for key, value in json.loads(data).items():
                self.__setitem__(key, value)
        except:
            pass

    def dumps(self):
        return json.dumps(self)


if __name__ == '__main__':
    d = Data('{"x": 1, "y": 2}')
    for key, value in d.items():
        print key, value
    print "dumps:", repr(d.dumps())
