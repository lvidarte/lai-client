# -*- coding: utf-8 -*-

import pymongo
from pymongo.errors import AutoReconnect
from lai import config
from lai.db.base import DBBase
from lai.database import DatabaseException, UPDATE_RESPONSE, COMMIT_RESPONSE
from lai import Document


class DBMongo(DBBase):

    def connect(self): 
        try: 
            self.connection = pymongo.Connection(self.config['HOST'],
                                                 self.config['PORT'])
            self.db = self.connection[self.config['NAME']]
            self.collection = self.db[self.config['TABLE']]
        except AutoReconnect:
            raise DatabaseException("It's not possible connect to the database")

    def get_last_tid(self):
        try:
            spec = {'tid': {'$gt': 0}}
            sort = [('tid', -1)]
            row = self.collection.find_one(spec, sort=sort)
        except Exception as e:
            DatabaseException(e)
        if row:
            return row['tid']
        return 0

    def get_next_id(self):
        try:
            query = {'_id': self.config['TABLE']}
            update = {'$inc': {'last_id': 1}}
            collection = self.db['counter']
            row = collection.find_and_modify(query, update,
                                             upsert=True, new=True)
        except Exception as e:
            DatabaseException(e)
        return row['last_id']

    def search(self, regex):
        try:
            spec = {'keys': {'$regex': regex}}
            fields = {'_id': 0}
            cur = self.collection.find(spec, fields)
        except Exception as e:
            DatabaseException(e)
        return [Document(**row) for row in cur]

    def status(self):
        return self.get_docs_for_commit()

    def get(self, id):
        try:
            spec = {'id': int(id)}
            fields = {'_id': 0}
            row = self.collection.find_one(spec, fields)
        except Exception as e:
            DatabaseException(e)
        if row:
            return Document(**row)
        return None

    def getall(self):
        try:
            cur = self.collection.find({}, {'_id': 0})
        except Exception as e:
            DatabaseException(e)
        return [Document(**row) for row in cur]

    def save(self, doc):
        if doc.id:
            return self.update(doc)
        else:
            return self.insert(doc)

    def insert(self, doc, synched=False):
        doc.id = self.get_next_id()
        doc.synched = synched
        try:
            self.collection.insert(doc.to_dict())
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def update(self, doc, type=None):
        if type is None:
            pk = 'id'
            id = doc.id
            doc.synched = False
            doc_ = doc.to_dict()
        elif type == UPDATE_RESPONSE:
            if self.collection.find({'sid': doc.sid}).count() == 0:
                return self.insert(doc, synched=True)
            if config.USER in doc.usersdel:
                doc.data = None
                doc.keys = None
            pk = 'sid'
            id = doc.sid
            doc.synched = True
            doc_ = doc.to_dict()
        elif type == COMMIT_RESPONSE:
            pk = 'id'
            id = doc.id
            doc.synched = True
            doc_ = {'sid': doc.sid, 'tid': doc.tid, 'synched': doc.synched}
            if config.USER in doc.usersdel:
                doc_.update(data=None, keys=None)
        else:
            raise DatabaseException('incorrect type')

        try:
            rs = self.collection.update({pk: id}, {'$set': doc_}, safe=True)
            assert rs['n'] == 1
        except Exception as e:
            raise DatabaseException(e)
        else:
            return doc

    def delete(self, doc):
        doc.data = None
        doc.keys = None
        return self.update(doc)

    def get_docs_for_commit(self):
        try:
            spec = {'synched': False}
            fields = {'_id': 0}
            cur = self.collection.find(spec, fields)
        except Exception as e:
            DatabaseException(e)
        return [Document(**row) for row in cur]

    def __str__(self):
        return "%s://%s:%s/%s?%s" % (self.config['ENGINE'],
                                     self.config['HOST'],
                                     self.config['PORT'],
                                     self.config['NAME'],
                                     self.config['TABLE'])

