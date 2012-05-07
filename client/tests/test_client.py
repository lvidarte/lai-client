# -*- coding: utf-8 -*-

import unittest
import client


class TestClient(unittest.TestCase):

    def test_get(self):
        assert type(client.get()) == list

    def test_get_max_transaction_id(self):
        assert type(client.get_max_transaction_id()) == int

