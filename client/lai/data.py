# -*- coding: utf-8 -*-

import json

class Data(dict):

    def __init__(self, data, key=None):
        self.key = key
        try:
            for k, v in json.loads(data).items():
                self.__setitem__(k, v)
            self.keys = self.get_keys()
        except:
            pass

    def dumps(self):
        return json.dumps(self)

    def get_keys(self):
        if self.key is not None:
            return self.__getitem__(self.key).split()
        else:
            return []


if __name__ == '__main__':
    d = Data('{"text": "Lorem ipsum dolor sit amet.", "value": 2}', key='text')
    for key, value in d.items():
        print key, value
    print "dumps:", repr(d.dumps())
    print "keys: ", d.keys
