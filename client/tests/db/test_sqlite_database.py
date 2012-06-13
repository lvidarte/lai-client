import unittest
import os.path
import config_sqlite
from db import DBSqlite

class TestDBSqlite(unittest.TestCase):

    def setUp(self):
        pass

    def test_connect_should_create_dbfile(self):
        db = DBSqlite(config_sqlite)
        self.assertTrue(os.path.exists(config_sqlite.DB_NAME))

