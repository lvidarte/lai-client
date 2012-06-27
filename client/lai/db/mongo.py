# -*- coding: utf-8 -*-

import pymongo
from lai.db.base import DBBase
from lai.database import UPDATE_RESPONSE, COMMIT_RESPONSE
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
        return 0

    def search(self, regex):
        cur = self.collection.find({'data': {'$regex': regex}})
        docs = []
        for row in cur:
            row['id'] = str(row['_id'])
            del row['_id']
            docs.append(Document(**row))
        return docs

    def get(self, id):
        rs = self.collection.find_one({'_id': ObjectId(id)})
        if rs:
            rs['id'] = str(rs['_id'])
            del rs['_id']
            doc = Document(**rs)
            return doc

    def save(self, doc):
        if doc.id:
            return self.update(doc)
        else:
            return self.insert(doc)

    def insert(self, doc):
        doc_ = {'sid'     : doc.sid,
                'tid'     : doc.tid,
                'data'    : doc.data,
                'keys'    : doc.keys,
                'users'   : doc.users,
                'usersdel': doc.usersdel,
                'synched' : False}
        rs = self.collection.insert(doc_)
        return str(rs)

    def update(self, doc, type=None):
        if type is None:
            pk = '_id'
            id = ObjectId(doc.id)
            upsert = False
            doc_ = {'sid'     : doc.sid,
                    'tid'     : doc.tid,
                    'data'    : doc.data,
                    'keys'    : doc.keys,
                    'users'   : doc.users,
                    'usersdel': doc.usersdel,
                    'synched' : False}
        elif type == UPDATE_RESPONSE:
            pk = 'sid'
            id = doc.id
            upsert = True
            doc_ = {'sid'     : doc.sid,
                    'tid'     : doc.tid,
                    'data'    : doc.data,
                    'keys'    : doc.keys,
                    'users'   : doc.users,
                    'usersdel': doc.usersdel,
                    'synched' : True}
        elif type == COMMIT_RESPONSE:
            pk = '_id'
            id = ObjectId(doc.id)
            upsert = False
            doc_ = {'sid'     : doc.sid,
                    'tid'     : doc.tid,
                    'synched' : True}
        else:
            return False

        rs = self.collection.update({pk: id},
                                    {'$set': doc_},
                                    safe=True,
                                    upsert=upsert)
        return rs['n'] == 1

    def get_docs_for_commit(self):
        rs = self.collection.find({'synched': False})
        docs = []
        for row in rs:
            row['id'] = str(row['_id'])
            del row['_id']
            del row['synched']
            docs.append(row)
        return docs

    def __str__(self):
        return "%s://%s:%s/%s?%s" % (self.config['ENGINE'],
                                     self.config['HOST'],
                                     self.config['PORT'],
                                     self.config['NAME'],
                                     self.config['TABLE'])

