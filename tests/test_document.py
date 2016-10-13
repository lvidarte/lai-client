# -*- coding: utf-8 -*-

# Author: Leo Vidarte <http://nerdlabs.com.ar>
#
# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

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

