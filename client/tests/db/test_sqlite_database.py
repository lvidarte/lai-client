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
        self.config = {'NAME': 'lai.db',
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
        new_doc = Document(sid=1, tid=2, data='sarlanga')
        self.db.save(new_doc)
        doc = self.db.get(1)
        self.assertEqual(doc.data, 'sarlanga')

    def test_update(self):
        new_doc = Document(data='1 2 3')
        self.db.save(new_doc)
        edit_doc = self.db.get(1)
        edit_doc.data = '1 2 3 4'
        self.db.save(edit_doc)
        
        doc = self.db.get(1)
        self.assertEqual(doc.data, '1 2 3 4')

