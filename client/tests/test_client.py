# -*- coding: utf-8 -*-

import unittest
from lai import config

config.DB_COLLECTION = 'docs_test'

import lai.client


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = "Testing data"
        cls.id = str(lai.client.add(cls.text))

    @classmethod
    def tearDownClass(cls):
        lai.client.delete(cls.id)

    def test_get(self):
        assert type(lai.client.get()) == list

    def test_get_by_id(self):
        docs = lai.client.get(self.id)
        assert type(docs) == list

    def test_put(self):
        new_data = "Other testing data"
        lai.client.put(self.id, new_data)
        docs = lai.client.get(self.id)
        assert docs[0]['data'] == new_data
        assert str(docs[0]['_id']) == self.id

    def test_get_last_tid(self):
        assert type(lai.client.get_last_tid()) == int

    def test_get_doc_for_commit(self):
        _doc = {'_id': 1,
                'tid': 2,
                'cid': 2, 
                'data': 'sarasa'}
        doc = lai.client.get_doc_for_commit(_doc)
        for key, value in doc.items():
            assert key in ('sid', 'tid', 'cid', 'data')

