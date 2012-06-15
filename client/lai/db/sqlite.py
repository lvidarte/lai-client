# -*- coding: utf-8 -*-

import sqlite3 as sqlite
from lai.db.base import DBBase


class DBSqlite(DBBase):

    def connect(self): 
        '''Connect to the database'''

        self.connection = sqlite.connect(self.config['NAME'])
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
                                   (id INTEGER PRIMARY KEY AUTOINCREMENT)
                                ''' % self.config['TABLE'])
        except Exception, e:
            print 'Error', e
            return False

        return True

    def __str__(self):
        return "%s://%s" % ('sqlite', self.config['NAME'])
