# -*- coding: utf-8 -*-

# Author: Leo Vidarte <http://nerdlabs.com.ar>
#
# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

import pymongo
from pymongo.errors import AutoReconnect
from lai.db.base import DBBase
from lai.database import UPDATE_PROCESS, COMMIT_PROCESS
from lai.database import DatabaseException, NotFoundError
from lai import Document


class DBMongo(DBBase):

    def __init__(self, name, host='127.0.0.1', port=27017):
        self.name = name
        self.host = host
        self.port = port

    def connect(self): 
        try:
            self.connection = pymongo.Connection(self.host, self.port)
            self.db = self.connection[self.name]
        except AutoReconnect:
            raise DatabaseException("It's not possible connect to the database")

    def get_next_id(self):
        try:
            query = {'_id': 'last_id'}
            update = {'$inc': {'id': 1}}
            fn = self.db.internal.find_and_modify
            row = fn(query, update, upsert=True, new=True)
        except Exception as e:
            raise DatabaseException(e)
        return row['id']

    def search(self, regex):
        try:
            spec = {'$or': [{'data.content'    : {'$regex': regex, '$options': 'im'}},
                            {'data.description': {'$regex': regex, '$options': 'im'}}]}
            fields = {'_id': 0}
            cur = self.db.docs.find(spec, fields)
        except Exception as e:
            raise DatabaseException(e)
        return [Document(**row) for row in cur]

    def get(self, id, pk='id', deleted=False):
        try:
            if pk == 'id':
                id = int(id)
            if deleted:
                spec = {pk: id}
            else:
                spec = {pk: id, 'data': {'$exists': 1}}
            fields = {'_id': 0}
            row = self.db.docs.find_one(spec, fields)
        except Exception as e:
            raise DatabaseException(e)
        if row:
            return Document(**row)
        raise NotFoundError('%s %s not found' % (pk, id))

    def getall(self):
        try:
            spec = {'data': {'$exists': 1}}
            fields = {'_id': 0}
            sort = [('tid', 1)]
            cur = self.db.docs.find(spec, fields, sort=sort)
        except Exception as e:
            raise DatabaseException(e)
        return [Document(**row) for row in cur]

    def save(self, doc):
        if doc.id:
            return self.update(doc)
        else:
            return self.insert(doc)

    def insert(self, doc, synced=False):
        doc.id = self.get_next_id()
        doc.synced = synced
        try:
            self.db.docs.insert(doc)
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def update(self, doc, process=None):
        if process is None:
            pk = 'id'
            id = doc.id
            doc.synced = False
            set = doc
        elif process == UPDATE_PROCESS:
            if self.db.docs.find({'sid': doc.sid}).count() == 0:
                return self.insert(doc, synced=True)
            pk = 'sid'
            id = doc.sid
            doc.synced = not doc.merged() # must be commited if was merged
            doc.merged(False)
            set = {'tid': doc.tid, 'data': doc.data, 'user': doc.user,
                   'public': doc.public, 'synced': doc.synced}
        elif process == COMMIT_PROCESS:
            pk = 'id'
            id = doc.id
            doc.synced = True
            set = {'sid': doc.sid, 'tid': doc.tid, 'synced': doc.synced}
        else:
            raise DatabaseException('Incorrect update process')

        try:
            rs = self.db.docs.update({pk: id}, {'$set': set}, safe=True)
            assert rs['n'] == 1
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def delete(self, doc):
        if doc.id is None:
            raise DatabaseException('Document does not have id')
        if doc.sid is None:
            try:
                rs = self.db.docs.remove({'id': doc.id}, safe=True)
                assert rs['n'] == 1
            except Exception as e:
                raise DatabaseException(e)
            return None
        doc.data = None
        return self.update(doc)

    def save_last_sync(self, ids, process):
        try:
            spec = {'_id': 'last_sync'}
            document = {'$set': {process: ids}}
            self.db.internal.update(spec, document, upsert=True)
        except Exception as e:
            raise DatabaseException(e)

    def get_docs_to_commit(self):
        try:
            spec = {'synced': False}
            fields = {'_id': 0}
            cur = self.db.docs.find(spec, fields)
        except Exception as e:
            raise DatabaseException(e)
        return list(cur)

    def get_last_tid(self):
        try:
            spec = {'tid': {'$gt': 0}}
            sort = [('tid', -1)]
            row = self.db.docs.find_one(spec, sort=sort)
        except Exception as e:
            raise DatabaseException(e)
        if row:
            return row['tid']
        return 0

    def status(self):
        docs = {'updated'  : [],
                'committed': [],
                'to_commit': []}

        row = self.db.internal.find_one({'_id': 'last_sync'})

        if row and 'update' in row:
            for id in row['update']:
                docs['updated'].append(self.get(id, deleted=True))

        if row and 'commit' in row:
            for id in row['commit']:
                docs['committed'].append(self.get(id, deleted=True))

        to_commit =  self.get_docs_to_commit()
        for row in to_commit:
            doc = Document(**row)
            docs['to_commit'].append(doc)
        return docs

    def __str__(self):
        return "%s://%s:%s/%s" % ('mongo', self.host, self.port, self.name)

