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
import os
from lai.db import DBSqlite
from lai    import Document


class TestDBSqlite(unittest.TestCase):

    def _delete_dbfile(self):
        try:
            os.remove(self.config['NAME'])
        except OSError:
            pass

    def setUp(self):
        self.config = {'NAME': 'lai_test.db',
                       'TABLE': 'client'}

        self.db = DBSqlite(self.config)

    def tearDown(self):
        self._delete_dbfile()

    def test_connect_should_create_dbfile(self):
        DBSqlite(self.config)
        self.assertTrue(os.path.exists(self.config['NAME']))

    def test_table_should_not_exists(self):
        self.assertFalse(self.db._table_exists('imposible_que_exista.db'))

    def test_table_creation(self):
        self.db.config['TABLE'] = 'Probando' 
        self.assertTrue(self.db._initialize_database())

    def test_docs_count(self):
        self.assertEqual(self.db.docs_count(), 0)

    def test_insert_new_document(self):
        doc = Document(data='probando probando', keys='nada')
        self.db.save(doc)
        self.assertEqual(self.db.docs_count(), 1)

    def test_get_doc_by_id(self):
        new_doc = Document(sid=1, tid=2, data='sarlanga', users=['alfredo', 'maria'])
        self.db.save(new_doc)
        doc = self.db.get(1)
        self.assertEqual(doc.data, 'sarlanga')
        self.assertEqual(doc.sid, '1')
        self.assertEqual(doc.tid, '2')
        self.assertEqual(doc.users, [u'alfredo', u'maria'])

    def test_update(self):
        new_doc = Document(data='1 2 3')
        self.db.save(new_doc)
        edit_doc = self.db.get(1)
        edit_doc.data = '1 2 3 4'
        self.db.save(edit_doc)

        doc = self.db.get(1)
        self.assertEqual(doc.data, '1 2 3 4')

    def test_get_last_tid(self):
        self.assertEqual(self.db.get_last_tid(),0)
    
    def test_exist(self):
        self.db.save(Document('git log --graph --oneline --all #fancy git log'))
        self.assertTrue(self.db._exists('id', 1))
        self.assertFalse(self.db._exists('id', 0))
        self.assertFalse(self.db._exists('id', None))

    def test_exist_with_sid(self):
        self.db.save(Document('git log --graph --oneline --all #fancy git log', sid=33))
        self.assertTrue(self.db._exists('sid', 33))
        self.assertFalse(self.db._exists('sid', 0))
        self.assertFalse(self.db._exists('sid', None))

    def test_search(self):
        '''guardo algunos documentos luego los busco por
           diferentes criterios'''

        self.db.save(Document('ls -l --color'))
        self.db.save(Document('git log --graph --oneline --all #fancy git log'))
        self.db.save(Document('can(){ shift 2; sudo "$@"; } #sudo like a sir'))
        self.db.save(Document('git fetcho upstream/aster'))

        res = self.db.search('ls')
        self.assertEqual(len(res), 1)

        res = self.db.search('git')
        self.assertEqual(len(res), 2)

        res = self.db.search('o')
        self.assertEqual(len(res), 4)

        res = self.db.search('Z')
        self.assertEqual(len(res), 0)

        res = self.db.search(None)
        self.assertEqual(len(res), 0)

        res = self.db.search('')
        self.assertEqual(len(res), 0)

    def test_get_docs_for_commit(self):

        self.db.save(Document('ls -l --color'))
        self.db.save(Document('git log --graph --oneline --all #fancy git log'))
        self.db.save(Document('can(){ shift 2; sudo "$@"; } #sudo like a sir'))
        self.db.save(Document('git fetcho upstream/aster'), synched=True)

        docs = self.db.get_docs_for_commit()
        self.assertEqual(len(docs), 3)
