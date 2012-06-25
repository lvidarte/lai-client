# -*- coding: utf-8 -*-

import sqlite3 as sqlite
from lai.db.base import DBBase
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
                                    tid      TEXT,
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

    def update(self, doc, synched=False, pk='id'):

        if pk == 'id':
            self.save(doc, synched)
        elif pk == 'sid':
            id = self._exists('sid', doc.sid)
            doc['id'] = id
            self.save(doc, synched)

    def get(self, id):

        self.cursor.execute('''SELECT * FROM %s
                              WHERE id = %d''' % (self.config['TABLE'], id))
        row = self.cursor.fetchone()
        if row is not None:
            doc = Document(**row)
            doc.users    = row[5].split(',')
            doc.usersdel = row[6].split(',')
        return doc

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
                               WHERE synched = 'False' ''' % (self.config['TABLE']))
        rows = self.cursor.fetchall()
        for row in rows:
            doc = Document(**row)
            doc.users    = row[5].split(',')
            doc.usersdel = row[6].split(',')
            docs.append(doc)
        return docs

    def get_last_tid(self):

        self.cursor.execute('''SELECT tid
                               FROM %s
                               ORDER BY tid DESC
                               LIMIT 1''' % (self.config['TABLE']))

        row = self.cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return 0

    def _create(self, doc, synched=False):

        sql_insert = '''INSERT INTO %s
           (tid, sid, data, keys, users, usersdel, synched)
           VALUES ('%s','%s','%s','%s', '%s', '%s', '%s')
        '''
        rows_afected = self.cursor.execute(sql_insert % (self.config['TABLE'],
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
                        SET sid      = '%s',
                            tid      = '%s',
                            data     = '%s',
                            keys     = '%s',
                            users    = '%s',
                            usersdel = '%s',
                            synched  = '%s'
                        WHERE id = %d
                     '''
        rows_afected = self.cursor.execute(sql_update % (self.config['TABLE'],
                                                         doc.sid,
                                                         doc.tid,
                                                         doc.data,
                                                         doc.keys,
                                                         ','.join(doc.users),
                                                         ','.join(doc.usersdel),
                                                         synched,
                                                         doc.id)).rowcount
        self.connection.commit()
        return rows_afected

    def _exists(self, key='id', value=None):

        if value:
            self.cursor.execute('''SELECT id FROM %s
                                   WHERE %s = %s''' % (self.config['TABLE'], key, value))
            return self.cursor.fetchone()[0]
        else:
            return False

    def docs_count(self):

        self.cursor.execute("SELECT COUNT(*) AS COUNT FROM %s" % self.config['TABLE'])
        return self.cursor.fetchone()[0]

    def __str__(self):
        return "%s://%s" % ('sqlite', self.config['NAME'])
