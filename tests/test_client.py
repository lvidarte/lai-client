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
from mockito import mock, when

from lai import Client
from lai import Document


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_save(self):
        database = mock()
        document = Document('Elena X')
        when(database).save(document).thenReturn(True)
        client = Client(database)
        result = client.save(document)
        self.assertTrue(result)

    def test_search_empty(self):
        database = mock()
        when(database).search('').thenReturn([])
        client = Client(database)
        result = client.search('')
        self.assertEquals(len(result), 0)

