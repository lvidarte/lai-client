import unittest
import os
from lai.db import DBSqlite


config = {'NAME': 'lai.db',
          'TABLE': 'client1'}


class TestDBSqlite(unittest.TestCase):

    def setUp(self):
        try:
            os.remove(config['NAME'])
        except OSError:
            pass
        self.db = DBSqlite(config)

    def test_connect_should_create_dbfile(self):
        DBSqlite(config)
        self.assertTrue(os.path.exists(config['NAME']))

    def test_table_should_not_exists(self):
        self.assertFalse(self.db._table_exists('imposible_que_exista.db'))

    def test_table_creation(self):
        self.assertTrue(self.db._initialize_database())
