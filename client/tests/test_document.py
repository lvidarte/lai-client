# -*- coding: utf-8 -*-

import unittest

from lai import Document


class TestDocument(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dict_doc = {
            "id":       4,
            "sid":      "4fb2745e47bce869ea000001",
            "tid":      2,
            "data":     "Lorem ipsum dolor sit amet in justo hendrerit vel posuere.",
            "keys":     "Lorem ipsum dolor amet hendrerit posuere",
            "users":    ["lvidarte"],
            "usersdel": []
        }

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_from_dict(self):
        doc = Document(self.dict_doc)
        self.assertEquals(doc.id, 4)
        self.assertEquals(doc.sid, "4fb2745e47bce869ea000001")

