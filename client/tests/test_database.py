# -*- coding: utf-8 -*-

import unittest

from lai import Database


class TestDatabaseMongo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_search(self):
        database = Database('mongo')
        result = database.search('')
        self.assertEquals(type(result), list)

