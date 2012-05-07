# -*- coding: utf-8 -*-

import unittest
import lai.client


class TestClient(unittest.TestCase):

    def test_get(self):
        assert type(lai.client.get()) == list

    def test_get_max_transaction_id(self):
        assert type(lai.client.get_max_transaction_id()) == int

