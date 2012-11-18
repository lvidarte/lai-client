# -*- coding: utf-8 -*-

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

import os.path
import sqlite3 as sqlite
import json

from lai.db.base import DBBase
from lai.database import UPDATE_PROCESS, COMMIT_PROCESS
from lai.database import DatabaseException, NotFoundError
from lai import Document


class DBSqlite(DBBase):

    def connect(self):
        database_exists = os.path.exists(self.config['NAME'])
        try:
            self.connection = sqlite.connect(self.config['NAME'])
            self.connection.row_factory = self._dict_factory
            self.cursor = self.connection.cursor()
            if not database_exists:
                self._initialize_database()
        except Exception as e:
            raise DatabaseException(e)

    def _dict_factory(self, cursor, row):
        '''Factory to return row as dict,
           converting data field into dict too'''
        d = {}
        for i, col in enumerate(cursor.description):
            key = col[0]
            value = row[i]
            if key == 'data':
                value = json.loads(value)
            if key in ('public', 'synced'):
                value = bool(value)
            d[key] = value
        return d

    def _initialize_database(self):
        '''Create the table if doesn't exists'''
        self.cursor.execute('''CREATE TABLE docs
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                sid      TEXT,
                                tid      INTEGER DEFAULT 0,
                                data     TEXT,
                                user     TEXT,
                                public   INTEGER DEFAULT 0,
                                synced   INTEGER DEFAULT 0)
                            ''')
        self.cursor.execute('''CREATE TABLE internal
                               (id   TEXT UNIQUE,
                                data TEXT)
                            ''')

    def search(self, regex):
        try:
            query = "SELECT * FROM docs WHERE data REGEXP ?"
            self.cursor.execute(query, (regex,))
            rows = self.cursor.fetchall()
        except Exception as e:
            raise DatabaseException(e)
        return [Document(**row) for row in rows]

    def get(self, id):
        try:
            self.cursor.execute('SELECT * FROM docs WHERE id=?', (id,))
            row = self.cursor.fetchone()
        except Exception as e:
            raise DatabaseException(e)
        if row:
            return Document(**row)
        raise NotFoundError('id %s not found' % id)

    def getall(self):
        try:
            query = '''SELECT * FROM docs
                       WHERE data is not null
                       ORDER BY tid DESC'''
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except Exception as e:
            raise DatabaseException(e)
        return [Document(**row) for row in rows]

    def save(self, doc):
        if doc.id:
            return self.update(doc)
        else:
            return self.insert(doc)

    def insert(self, doc, synced=False):
        doc.synced = synced
        query = '''INSERT INTO docs
                   (tid, sid, data, user, public, synced)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        args = (doc.tid, doc.sid, json.dumps(doc.data),
                doc.user, int(doc.public), int(doc.synced))
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            doc.id = self.cursor.lastrowid
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def update(self, doc, type=None):
        if type is None:
            doc.synced = False
            query = """UPDATE docs SET data=?, user=?, public=?, synced=?
                       WHERE id=?"""
            args = (json.dumps(doc.data), doc.user, int(doc.public),
                    int(doc.synced), doc.id)

        elif type == UPDATE_PROCESS:
            self.cursor.execute("SELECT id FROM docs WHERE sid=?", (doc.sid,))
            if self.cursor.fetchone() is None:
                return self.insert(doc, synced=True)
            doc.synced = True
            query = """UPDATE docs
                       SET tid=?, data=?, user=?, public=?, synced=?
                       WHERE sid=?"""
            args = (doc.tid, json.dumps(doc.data), doc.user,
                    int(doc.public), int(doc.synced), doc.sid)

        elif type == COMMIT_PROCESS:
            doc.synced = True
            query = "UPDATE docs SET sid=?, tid=?, synced=? WHERE id=?"
            args = (doc.sid, doc.tid, int(doc.synced), doc.id)
        else:
            raise DatabaseException('Incorrect update type')

        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            assert self.cursor.rowcount == 1
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def delete(self, doc):
        if doc.id is None:
            raise DatabaseException('Document does not have id')
        if doc.sid is None:
            try:
                self.cursor.execute('DELETE FROM docs WHERE id=?', (doc.id))
                self.connection.commit()
                assert self.cursor.rowcount == 1
            except Exception as e:
                raise DatabaseException(e)
            return None
        doc.data = None
        return self.update(doc)

    def save_last_sync(self, process, ids):
        try:
            self.cursor.execute("""SELECT data FROM internal
                                   WHERE id='last_sync'""")
            row = self.cursor.fetchone()
            if row:
                data = row['data']
                data[process] = ids
            else:
                data = {process: ids}
            args = (json.dumps(data),)
            self.cursor.execute("""UPDATE internal SET data=?
                                   WHERE id='last_sync'""", args)
        except Exception as e:
            raise DatabaseException(e)

    def get_docs_to_commit(self):
        try:
            self.cursor.execute('SELECT * FROM docs WHERE synched=0')
            rows = self.cursor.fetchall()
        except Exception as e:
            raise DatabaseException(e)
        return rows

    def get_last_tid(self):
        try:
            self.cursor.execute('SELECT tid FROM docs ORDER BY tid DESC')
            row = self.cursor.fetchone()
        except Exception as e:
            raise DatabaseException(e)
        if row:
            return row['tid']
        return 0

    def status(self):
        docs = {'updated'  : [],
                'committed': [],
                'to_commit': []}

        self.cursor.execute("""SELECT data FROM internal
                               WHERE id='last_sync'""")
        row = self.cursor.fetchone()
        if row:
            data = json.loads(row['data'])
        else:
            data = {}

        if 'update' in data:
            for id in data['update']:
                docs['updated'].append(self.get(id))

        if 'commit' in data:
            for id in data['commit']:
                docs['committed'].append(self.get(id))

        to_commit = self.get_docs_to_commit()
        for row in to_commit:
            doc = Document(**row)
            docs['to_commit'].append(doc)
        return docs

    def __str__(self):
        return "%s://%s" % ('sqlite', self.config['NAME'])

