# -*- coding: utf-8 -*-

import pymongo
from lai.db.base import DBBase
from lai import Document

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

    def get(self, id):
        rs = self.collection.find_one({'_id': ObjectId(id)})
        if rs:
            document = Document()
            document.set(rs)
            document.id = str(rs['_id'])
            return document

    def save(self, document):
        doc = {
            'sid'     : document.sid,
            'tid'     : document.tid,
            'data'    : document.data,
            'keys'    : document.keys,
            'users'   : document.users,
            'usersdel': document.usersdel,
            'synched' : False,
        }
        if document.id:
            _id = ObjectId(document.id)
            rs = self.collection.update({'_id': _id}, {'$set': doc}, safe=True)
            return rs['n'] == 1
        else:
            rs = self.collection.insert(doc)
            return str(rs)

    def __str__(self):
        return "%s://%s:%s/%s?%s" % (self.config['ENGINE'],
                                     self.config['HOST'],
                                     self.config['PORT'],
                                     self.config['NAME'],
                                     self.config['TABLE'])

