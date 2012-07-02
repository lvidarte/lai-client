# -*- coding: utf-8 -*-

import sqlite3 as sqlite
from lai.db.base import DBBase
from lai.database import UPDATE_RESPONSE, COMMIT_RESPONSE
from lai import Document

class DBSqlite(DBBase):

    def connect(self): 
        '''Connect to the database'''

        self.connection = sqlite.connect(self.config['NAME'])
        self.connection.row_factory = sqlite.Row
        self.cursor = self.connection.cursor()

        if not self._table_exists():
            self._initialize_database()

    def _table_exists(self, table=None):
        '''Verify if the table was created'''

        if table is None:
            table = self.config['TABLE']
        self.cursor.execute('''SELECT name
                               FROM sqlite_master
                               WHERE type='table'
                               AND name='%s'
                            ''' % table)
        return (self.cursor.fetchone() is not None)

    def _initialize_database(self):
        '''Create the table if doesn't exists'''

        try:
            self.cursor.execute('''CREATE TABLE %s
                                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    sid      TEXT,
                                    tid      INTEGER DEFAULT 0,
                                    data     TEXT,
                                    keys     TEXT,
                                    users    TEXT,
                                    usersdel TEXT,
                                    synched  INTEGER DEFAULT 0)
                                ''' % self.config['TABLE'])
        except Exception, e:
            print 'Error', e
            return False
        return True

    def save(self, doc, synched=False):

        if doc.id is None:
            return self._create(doc, synched)
        else:
            return self._update(doc, synched)

    #def update(self, doc, synched=False, pk='id'):
    def update(self, doc, type=None):
        if type is None or type == UPDATE_RESPONSE:
            id = self._exists('sid', doc.sid)
            doc.id = id
            synched = True if type == UPDATE_RESPONSE else False
            self.save(doc, synched)
        elif COMMIT_RESPONSE:
            self._update_transaction(doc, synched=True)



    def get(self, id):

        self.cursor.execute('''SELECT * FROM %s
                              WHERE id = %s''' % (self.config['TABLE'], id))
        row = self.cursor.fetchone()
        if row is not None:
            doc = Document(**row)
            doc.users    = row[5].split(',')
            doc.usersdel = row[6].split(',')
        return doc
    
    def delete(self, doc):

        rc = self.connection.execute('''UPDATE %s 
                                          SET data=NULL, keys=NULL, synched=0 
                                          WHERE id = %s''' % (self.config['TABLE'], doc.id)).rowcount
        self.connection.commit()
        return rc

    def search(self, search_text):

        docs = []
        if (search_text is not None) and (not search_text == ''):
            self.cursor.execute('''SELECT * FROM %s
                                   WHERE data LIKE '%s' ''' % (self.config['TABLE'],
                                                               '%' + search_text + '%'))
            rows = self.cursor.fetchall()
            for row in rows:
                doc = Document(**row)
                doc.users    = row[5].split(',')
                doc.usersdel = row[6].split(',')
                docs.append(doc)
        return docs

    def get_docs_for_commit(self):

        docs = []
        self.cursor.execute('''SELECT * FROM %s
                               WHERE synched = 0 ''' % (self.config['TABLE']))
        rows = self.cursor.fetchall()
        for row in rows:
            doc = Document(**row)
            doc.users    = row[5].split(',')
            doc.usersdel = row[6].split(',')
            docs.append(doc.to_dict())
        return docs

    def get_last_tid(self):

        self.cursor.execute('''SELECT tid
                               FROM %s
                               ORDER BY tid DESC
                               LIMIT 1''' % (self.config['TABLE']))

        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0

    def _create(self, doc, synched=False):

        sql_insert = '''INSERT INTO %s
           (tid, sid, data, keys, users, usersdel, synched)
           VALUES (?, ?, ?, ?, ?, ?, ?)
        ''' % self.config['TABLE']
        rows_afected = self.cursor.execute(sql_insert, (
                                          doc.tid,
                                          doc.sid,
                                          doc.data,
                                          doc.keys,
                                          ','.join(doc.users),
                                          ','.join(doc.usersdel),
                                          synched)).rowcount
        self.connection.commit()
        return rows_afected

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

        rows_afected = self.cursor.execute(sql_update, (doc.sid,
                                                       doc.tid,
                                                       doc.data,
                                                       doc.keys,
                                                       ','.join(doc.users),
                                                       ','.join(doc.usersdel),
                                                       synched)).rowcount
        self.connection.commit()
        return rows_afected

    def _update_transaction(self, doc, synched=False):

        sql_update = '''UPDATE %s
                        SET sid      = ?,
                            tid      = ?,
                            synched  = ?
                        WHERE id = %d
                     ''' % (self.config['TABLE'], doc.id)

        rows_afected = self.cursor.execute(sql_update, (doc.sid,
                                                        doc.tid,
                                                        synched)).rowcount
        self.connection.commit()
        return rows_afected

    def _exists(self, key='id', value=None):

        if value:
            self.cursor.execute('''SELECT id FROM %s
                                   WHERE %s = ?''' % (self.config['TABLE'], key),
                                   (value,))
            row = self.cursor.fetchone()
            if row:
                return row['id']
        else:
            return False

    def docs_count(self):

        self.cursor.execute("SELECT COUNT(*) AS COUNT FROM %s" % self.config['TABLE'])
        return self.cursor.fetchone()[0]

    def __str__(self):
        return "%s://%s" % ('sqlite', self.config['NAME'])
