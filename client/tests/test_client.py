# -*- coding: utf-8 -*-

import unittest
from mockito import mock, when

from lai import Client


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_search_empty(self):
        database = mock()
        when(database).search('').thenReturn([])
        client = Client(database)
        result = client.search('')
        self.assertEquals(len(result), 0)

