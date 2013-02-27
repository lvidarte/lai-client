# -*- coding: utf-8 -*-

# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

import MySQLdb as mysql
from MySQLdb.cursors import DictCursor
import json
import re

from lai.db.base import DBBase
from lai.database import UPDATE_PROCESS, COMMIT_PROCESS
from lai.database import DatabaseException, NotFoundError
from lai import Document


class DBMySQL(DBBase):

    def connect(self):
        try:
            args = {
                'host': self.config['HOST'],
                'port': self.config.get('PORT', 3306),
                'user': self.config['USER'],
                'passwd': self.config.get('PASSWD', ''),
                'db': self.config['NAME'],
                'cursorclass': DictCursor,
                }
            self.connection = mysql.connect(**args)
            self.cursor = self.connection.cursor()
            self._initialize_database()
        except Exception as e:
            raise DatabaseException(e)

    def _initialize_database(self):
        if self.cursor.execute("SHOW TABLES LIKE 'lai_%'") == 0:
            self.cursor.execute('''
                CREATE TABLE lai_docs
                   (`id`     int(11) NOT NULL AUTO_INCREMENT,
                    `sid`    varchar(24),
                    `tid`    int(11),
                    `data`   text,
                    `user`   varchar(256) NOT NULL,
                    `public` tinyint(1) NOT NULL DEFAULT 0,
                    `synced` tinyint(1) NOT NULL DEFAULT 0,
                    PRIMARY KEY (`id`),
                    KEY `IDX_LAI_DATA` (`data`(64))
                   )
                   ENGINE=InnoDB
                   AUTO_INCREMENT=0
                   DEFAULT CHARSET=utf8
                ''')
            self.cursor.execute('''
                CREATE TABLE lai_internal
                   (`id`   varchar(24) NOT NULL UNIQUE,
                    `data` text NOT NULL,
                    PRIMARY KEY (`id`)
                   )
                   ENGINE=InnoDB
                   DEFAULT CHARSET=utf8
                ''')

    def _match(self, regexp, data):
        content = data['content']
        description = data['description'] or ''
        return regexp.search(content) is not None or \
               regexp.search(description) is not None

    def search(self, regex):
        try:
            self.cursor.execute('''SELECT * FROM lai_docs
                                   WHERE data IS NOT NULL''')
        except Exception as e:
            raise DatabaseException(e)

        regexp = re.compile(regex)
        rows = []
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            row['data'] = json.loads(row['data'])
            if self._match(regexp, row['data']):
                rows.append(row)
        return [Document(**row) for row in rows]

    def get(self, id, pk='id', deleted=False):
        try:
            if deleted:
                query = 'SELECT * FROM lai_docs WHERE %s=%%s' % pk
            else:
                query = '''SELECT * FROM lai_docs
                           WHERE %%s=%s AND data IS NOT NULL''' % pk
            self.cursor.execute(query, id)
            row = self.cursor.fetchone()
        except Exception as e:
            raise DatabaseException(e)
        if row:
            return Document(**row)
        raise NotFoundError('%s %s not found' % (pk, id))

    def getall(self):
        try:
            self.cursor.execute('''SELECT * FROM lai_docs
                                   WHERE data IS NOT NULL
                                   ORDER BY tid DESC''')
            rows = self.cursor.fetchall()
        except Exception as e:
            raise DatabaseException(e)
        return [Document(**row) for row in rows]

    def save(self, doc):
        if doc.id:
            return self.update(doc)
        else:
            return self.insert(doc)

    def insert(self, doc, synced=False):
        doc.synced = synced
        query = '''INSERT INTO lai_docs
                   (tid, sid, data, user, public, synced)
                   VALUES (%s, %s, %s, %s, %s, %s)'''
        args = (doc.tid, doc.sid, json.dumps(doc.data),
                doc.user, int(doc.public), int(doc.synced))
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            doc.id = self.cursor.lastrowid
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def update(self, doc, process=None):
        merged = doc.merged()
        data = doc.data
        if data is not None:
            doc.merged(False)
            data = json.dumps(doc.data)

        if process is None:
            doc.synced = False
            query = """UPDATE lai_docs
                       SET data=%s, user=%s, public=%s, synced=%s
                       WHERE id=%s"""
            args = (data, doc.user, int(doc.public), int(doc.synced), doc.id)

        elif process == UPDATE_PROCESS:
            self.cursor.execute("SELECT id FROM lai_docs WHERE sid=%s",
                                doc.sid)
            if self.cursor.fetchone() is None:
                return self.insert(doc, synced=True)
            doc.synced = not merged # must be commited if was merged
            query = """UPDATE lai_docs
                       SET tid=%s, data=%s, user=%s, public=%s, synced=%s
                       WHERE sid=%s"""
            args = (doc.tid, data, doc.user,
                    int(doc.public), int(doc.synced), doc.sid)

        elif process == COMMIT_PROCESS:
            doc.synced = True
            query = "UPDATE lai_docs SET sid=%s, tid=%s, synced=%s WHERE id=%s"
            args = (doc.sid, doc.tid, int(doc.synced), doc.id)
        else:
            raise DatabaseException('Incorrect update process')

        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            assert self.cursor.rowcount == 1
        except Exception as e:
            raise DatabaseException(e)
        return doc

    def delete(self, doc):
        if doc.id is None:
            raise DatabaseException('Document does not have id')
        if doc.sid is None:
            try:
                self.cursor.execute('DELETE FROM lai_docs WHERE id=%s', doc.id)
                self.connection.commit()
                assert self.cursor.rowcount == 1
            except Exception as e:
                raise DatabaseException(e)
            return None
        doc.data = None
        return self.update(doc)

    def save_last_sync(self, ids, process):
        try:
            self.cursor.execute("""SELECT data FROM lai_internal
                                   WHERE id='last_sync'""")
            row = self.cursor.fetchone()
            if row:
                data = json.loads(row['data'])
                data[process] = ids
                args = (json.dumps(data),)
                query = "UPDATE lai_internal SET data=%s WHERE id='last_sync'"
            else:
                args = ('last_sync', json.dumps({process: ids}))
                query = "INSERT INTO lai_internal (id, data) VALUES (%s, %s)"

            self.cursor.execute(query, args)
            self.connection.commit()
        except Exception as e:
            raise DatabaseException(e)

    def get_docs_to_commit(self):
        try:
            self.cursor.execute('SELECT * FROM lai_docs WHERE synced=0')
            rows = self.cursor.fetchall()
        except Exception as e:
            raise DatabaseException(e)
        if rows is None:
            rows = []
        return rows

    def get_last_tid(self):
        try:
            self.cursor.execute('SELECT tid FROM lai_docs ORDER BY tid DESC')
            row = self.cursor.fetchone()
        except Exception as e:
            raise DatabaseException(e)
        if row:
            return row['tid']
        return 0

    def status(self):
        docs = {'updated'  : [],
                'committed': [],
                'to_commit': []}

        self.cursor.execute("""SELECT data FROM lai_internal
                               WHERE id='last_sync'""")
        row = self.cursor.fetchone()
        if row['data'] is None:
            data = {}
        else:
            data = json.loads(row['data'])

        if 'update' in data:
            for id in data['update']:
                docs['updated'].append(self.get(id, deleted=True))

        if 'commit' in data:
            for id in data['commit']:
                docs['committed'].append(self.get(id, deleted=True))

        to_commit = self.get_docs_to_commit()
        for row in to_commit:
            doc = Document(**row)
            docs['to_commit'].append(doc)
        return docs

    def __str__(self):
        return "%s://%s:%s/%s" % (self.config['ENGINE'],
                                  self.config['HOST'],
                                  self.config['PORT'],
                                  self.config['NAME'])


