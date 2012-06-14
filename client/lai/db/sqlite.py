# -*- coding: utf-8 -*-

import sqlite3 as sqlite
from lai.db.base import DBBase


class DBSqlite(DBBase):

    def connect(self): 
        self.connection = sqlite.connect(self.config['NAME'])
        if not self._table_exists(self.config['TABLE']):
            self._initialize_database()

    def _table_exists(self, table):
        pass

    def _initialize_database(self):
        pass

    def __str__(self):
        return "%s://%s" % ('sqlite', self.config['NAME'])
