import sqlite3 as sqlite
from db import DBBase

class DBSqlite(DBBase):

    def connect(self): 
        self.name  = self._config.DB_NAME
        self.table = self._config.DB_TABLE

        self.connection = sqlite.connect(self.name)

        if not self._table_exists(self.table):
            self._initialize_database()

    def _table_exists(self, table):
        pass

    def _initialize_database(self):
        pass
