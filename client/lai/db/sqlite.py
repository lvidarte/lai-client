# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite
from lai.db.base import DBBase
from lai import Document

class DBSqlite(DBBase):

    def connect(self): 
        '''Connect to the database'''

        self.connection = sqlite.connect(self.config['NAME'])

        self.cursor = self.connection.cursor()
        #self.cursor.execute("SELECT load_extension('%s')" % (self.config['REGEXP_EXTENSION_PATH']))
        #self.cursor.execute("SELECT load_extension('/usr/lib/sqlite3/pcre.so')")

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

    def save(self, doc):
        if doc.id is None:
            self._create(doc)
        else:
            self._update(doc)

    def get(self, id):
       self.cursor.execute('''SELECT * FROM %s
                              WHERE id = %d''' % (self.config['TABLE'], id))
       doc = Document()
       row = self.cursor.fetchone()

       if row is not None:
           doc.id       = row[0]
           doc.sid      = row[1]
           doc.tid      = row[2]
           doc.data     = row[3]
           doc.keys     = row[4]
           doc.users    = row[5].split(',')
           doc.usersdel = row[6].split(',')
       return doc

    def search(self, regex):
        self.cursor.execute('''SELECT data
                             FROM %s
                             WHERE data LIKE '%s' ''' % (
                                 self.config['TABLE'],
                                 '%' + regex + '%'))
        return self.cursor.fetchall()

    def get_docs_for_commit(self):
        self.cursor.execute('''SELECT * FROM %s
                               WHERE synched = 0''' % (self.config['TABLE']))

        return self.cursor.fetchall()

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

    def _create(self, doc):
        sql_insert = '''INSERT INTO %s
           (tid, sid, data, keys, users, usersdel, synched)
           VALUES ('%s','%s','%s','%s', '%s', '%s', %s)
        '''
        self.cursor.execute(sql_insert % (self.config['TABLE'],
                                          doc.tid,
                                          doc.sid,
                                          doc.data,
                                          doc.keys,
                                          ', '.join(doc.users),
                                          ', '.join(doc.usersdel),
                                          0))
        self.connection.commit()

    def _update(self, doc):
        sql_update = '''UPDATE %s
                        SET sid      = '%s',
                            tid      = '%s',
                            data     = '%s',
                            keys     = '%s',
                            users    = '%s',
                            usersdel = '%s'
                        WHERE id = %d
                     '''

        self.cursor.execute(sql_update % (self.config['TABLE'],
                                          doc.sid, doc.tid, doc.data,
                                          doc.keys,
                                          ', '.join(doc.users),
                                          ', '.join(doc.usersdel),
                                          doc.id))
        self.connection.commit()

    def docs_count(self):
        self.cursor.execute("SELECT COUNT(*) AS COUNT FROM %s" % self.config['TABLE'])
        return self.cursor.fetchone()[0]

    def __str__(self):
        return "%s://%s" % ('sqlite', self.config['NAME'])
