# -*- coding: utf-8 -*-

import pymongo
from lai.db.base import DBBase

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId


class DBMongo(DBBase):

    def connect(self): 
        self.connection = pymongo.Connection(self.config['HOST'],
                                             self.config['PORT'])
        self.db = self.connection[self.config['NAME']]
        self.collection = self.db[self.config['TABLE']]

    def get_last_tid(self):
        try:
            docs = self.collection.find({'tid': {'$gt': 0}})
            docs = docs.sort('tid', -1).limit(1)
            return int(docs.next()['tid'])
        except StopIteration:
            return 0

    def search(self, regex):
        return list(self.collection.find({'data': {'$regex': regex}}))

    def __str__(self):
        return "%s://%s:%s/%s?%s" % ('mongo',
                                     self.config['HOST'],
                                     self.config['PORT'],
                                     self.config['NAME'],
                                     self.config['TABLE'])

