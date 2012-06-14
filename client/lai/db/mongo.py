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

    def search(self, regex):
        return list(self.collection.find({'data': {'$regex': regex}}))

    def __str__(self):
        return "%s://%s:%s/%s?%s" % ('mongo',
                                     self.config['HOST'],
                                     self.config['PORT'],
                                     self.config['NAME'],
                                     self.config['TABLE'])

