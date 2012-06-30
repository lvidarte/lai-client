# -*- coding: utf-8 -*-

import pymongo
from lai.db.base import DBBase
from lai.database import UPDATE_RESPONSE, COMMIT_RESPONSE
from lai import Document


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

    def get_next_id(self):
        query = {'_id': self.config['TABLE']}
        update = {'$inc': {'last_id': 1}}
        collection = self.db['counter']
        row = collection.find_and_modify(query, update, upsert=True, new=True)
        return row['last_id']

    def search(self, regex):
        spec = {'data': {'$regex': regex}}
        fields = {'_id': 0}
        cur = self.collection.find(spec, fields)
        docs = []
        for row in cur:
            docs.append(Document(**row))
        return docs

    def get(self, id):
        spec = {'id': int(id)}
        fields = {'_id': 0}
        row = self.collection.find_one(spec, fields)
        if row:
            doc = Document(**row)
            return doc

    def save(self, doc):
        if doc.id:
            return self.update(doc)
        else:
            return self.insert(doc)

    def insert(self, doc):
        doc_ = {'id'      : self.get_next_id(),
                'sid'     : doc.sid,
                'tid'     : doc.tid,
                'data'    : doc.data,
                'keys'    : doc.keys,
                'users'   : doc.users,
                'usersdel': doc.usersdel,
                'synched' : False}
        rs = self.collection.insert(doc_)
        if rs:
            row = self.collection.find_one({'_id': rs})
            return row['id']
        return  False

    def update(self, doc, type=None):
        if type is None:
            pk = 'id'
            id = doc.id
            doc_ = {'sid'     : doc.sid,
                    'tid'     : doc.tid,
                    'data'    : doc.data,
                    'keys'    : doc.keys,
                    'users'   : doc.users,
                    'usersdel': doc.usersdel,
                    'synched' : False}
        elif type == UPDATE_RESPONSE:
            if self.collection.find({'sid': doc.sid}).count() == 0:
                return self.insert(doc)
            pk = 'sid'
            id = doc.sid
            doc_ = {'sid'     : doc.sid,
                    'tid'     : doc.tid,
                    'data'    : doc.data,
                    'keys'    : doc.keys,
                    'users'   : doc.users,
                    'usersdel': doc.usersdel,
                    'synched' : True}
        elif type == COMMIT_RESPONSE:
            pk = 'id'
            id = doc.id
            doc_ = {'sid'     : doc.sid,
                    'tid'     : doc.tid,
                    'synched' : True}
        else:
            return False

        rs = self.collection.update({pk: id}, {'$set': doc_}, safe=True)
        return rs['n'] == 1

    def delete(self, doc):
        spec = {'id': doc.id}
        document = {'$set': {'data': None, 'keys': None}}
        rs = self.collection.update(spec, document, safe=True)
        return rs['n'] == 1

    def get_docs_for_commit(self):
        spec = {'synched': False}
        fields = {'_id': 0, 'synched': 0}
        rs = self.collection.find(spec, fields)
        docs = []
        for row in rs:
            docs.append(row)
        return docs

    def __str__(self):
        return "%s://%s:%s/%s?%s" % (self.config['ENGINE'],
                                     self.config['HOST'],
                                     self.config['PORT'],
                                     self.config['NAME'],
                                     self.config['TABLE'])
