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

    def get_last_tid(self):
        doc = self.collection.find_one({'tid': {'$gt': 0}}, sort=[('tid', -1)])
        if doc:
            return doc['tid']
        else:
            return 0

    def search(self, regex):
        return list(self.collection.find({'data': {'$regex': regex}}))

    def get(self, id):
        rs = self.collection.find_one({'_id': ObjectId(id)})
        if rs:
            doc = Document()
            doc.set(rs)
            doc.id = str(rs['_id'])
            return doc

    def save(self, doc):
        doc_ = {
            'sid'     : doc.sid,
            'tid'     : doc.tid,
            'data'    : doc.data,
            'keys'    : doc.keys,
            'users'   : doc.users,
            'usersdel': doc.usersdel,
            'synched' : False,
        }
        if doc.id:
            doc_['id'] = doc.id
            return self.update(doc_, synched=False)
        else:
            rs = self.collection.insert(doc_)
            return str(rs)

    def update(self, doc, synched, pk='_id'):
        if pk == '_id':
            id = ObjectId(doc['id'])
            del doc['id']
            upsert = False
        elif pk == 'sid':
            id = doc['sid']
            upsert = True
        doc['synched'] = synched
        rs = self.collection.update({pk: id},
                                    {'$set': doc},
                                    safe=True,
                                    upsert=upsert)
        return rs['n'] == 1

    def get_docs_for_commit(self):
        rs = self.collection.find({'synched': False})
        docs = []
        for doc in rs:
            doc['id'] = str(doc['_id'])
            del doc['_id']
            docs.append(doc)
        return docs


    def __str__(self):
        return "%s://%s:%s/%s?%s" % (self.config['ENGINE'],
                                     self.config['HOST'],
                                     self.config['PORT'],
                                     self.config['NAME'],
                                     self.config['TABLE'])

