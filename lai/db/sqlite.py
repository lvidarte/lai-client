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
        self.cursor.execute('''CREATE TABLE internals
                               (id   TEXT UNIQUE,
                                data TEXT)
                            ''')

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
                doc.user, doc.public, doc.synced)
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
            query = """UPDATE docs SET (data=?, user=?, public=?, synced=?)
                       WHERE id=?"""
            args = (json.dumps(doc.data), doc.user, doc.public, doc.synced)

        elif type == UPDATE_PROCESS:
            self.cursor.execute("SELECT id FROM docs WHERE sid=?", (doc.sid,))
            if self.cursor.fetchone() is None:
                return self.insert(doc, synced=True)
            doc.synced = True
            query = """UPDATE docs
                       SET (tid=?, data=?, user=?, public=?, synced=?)
                       WHERE sid=?"""
            args = (doc.tid, json.dumps(doc.data), doc.user,
                    doc.public, doc.synced, doc.sid)

        elif type == COMMIT_PROCESS:
            doc.synced = True
            query = "UPDATE docs SET (sid=?, tid=?, synced=?) WHERE id=?"
            args = (doc.sid, doc.tid, doc.synced, doc.id)
        else:
            raise DatabaseException('Incorrect update type')

        try:
            self.cursor.execute(query, args)
            assert self.cursor.rowcount == 1
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def delete(self, doc):
        try:
            rc = self.connection.execute('''UPDATE %s
                                          SET data=NULL, keys=NULL, synched=0
                                          WHERE id = %s''' % (self.config['TABLE'], doc.id))
            self.connection.commit()
        except Exception as e:
            DatabaseException(e)
        else:
            return True

    def search(self, search_text):

        docs = []
        try:
            if (search_text is not None) and (not search_text == ''):
                self.cursor.execute('''SELECT * FROM %s
                                       WHERE keys LIKE '%s' ''' % (self.config['TABLE'],
                                                                   '%' + search_text + '%'))
                rows = self.cursor.fetchall()
                for row in rows:
                    doc = Document(**row)
                    doc.users    = row[5].split(',')
                    doc.usersdel = row[6].split(',')
                    docs.append(doc)
        except Exception as e:
            DatabaseException(e)
        else:
            return docs

    def get_docs_for_commit(self):

        docs = []
        try:
            self.cursor.execute('''SELECT * FROM %s
                                   WHERE synched = 0 ''' % (self.config['TABLE']))
            rows = self.cursor.fetchall()
            for row in rows:
                doc = Document(**row)
                doc.users    = row[5].split(',')
                doc.usersdel = row[6].split(',')
                docs.append(doc.to_dict())
        except Exception as e:
            DatabaseException(e)
        else:
            return docs

    def get_last_tid(self):

        try:
            self.cursor.execute('''SELECT tid
                                   FROM %s
                                   ORDER BY tid DESC''' % (self.config['TABLE']))

            row = self.cursor.fetchone()
        except Exception as e:
            raise DatabaseException(e)
        else:
            if row is not None:
                return row[0]
            else:
                return 0

    def status(self):
        docs = []
        dfcs = self.get_docs_for_commit()
        for dfc in dfcs:
            doc = Document(**dfc)
            docs.append(doc)
        return docs

    def _update(self, doc, synched=False):

        sql_update = '''UPDATE %s
                        SET sid      = ?,
                            tid      = ?,
                            data     = ?,
                            keys     = ?,
                            users    = ?,
                            usersdel = ?,
                            synched  = ?
                        WHERE id = %d
                     ''' % (self.config['TABLE'], doc.id)
        try:
            args =  (doc.sid, doc.tid, doc.data, doc.keys,
                    ','.join(doc.users), ','.join(doc.usersdel), synched)
            rs = self.cursor.execute(sql_update, args)
            self.connection.commit()
        except Exception as e:
            raise DatabaseException(e)
        else:
            return doc

    def _update_transaction(self, doc, synched=False):

        sql_update = '''UPDATE %s
                        SET sid      = ?,
                            tid      = ?,
                            synched  = ?
                        WHERE id = %d
                     ''' % (self.config['TABLE'], doc.id)
        try:
            args = (doc.sid, doc.tid, synched)
            rs = self.cursor.execute(sql_update, args)
            self.connection.commit()
        except Exception as e:
            raise DatabaseException(e)
        else:
            return doc

    def _exists(self, key='id', value=None):

        if value:
            try:
                self.cursor.execute('''SELECT id FROM %s
                                   WHERE %s = ?''' % (self.config['TABLE'], key),
                                   (value,))
                row = self.cursor.fetchone()
            except Exception as e:
                DatabaseException(e)
            else:
                if row is not None:
                    return row['id']
        else:
            return False

    def _create_doc(self, row):
        pass

    def docs_count(self):

        self.cursor.execute("SELECT COUNT(*) AS COUNT FROM %s" % self.config['TABLE'])
        return self.cursor.fetchone()[0]

    def __str__(self):
        return "%s://%s" % ('sqlite', self.config['NAME'])
