import unittest
import os.path
from lai.db import DBSqlite


config = {'NAME': 'lai.db',
          'TABLE': 'client1'}


class TestDBSqlite(unittest.TestCase):

    def setUp(self):
        pass

    def test_connect_should_create_dbfile(self):
        db = DBSqlite(config)
        self.assertTrue(os.path.exists(config['NAME']))

