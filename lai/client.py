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

import urllib
import urllib2
import json
import base64

from lai import config
from lai.document import Document
from lai.database import UPDATE_PROCESS, COMMIT_PROCESS
from lai.database import NotFoundError
from lai.lib import crypto


CLIENT_PRV_KEY = open(config.PRV_KEY_PATH, 'r').read()


class Client:

    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.session_id = None

    def sync(self, docs=None):
        conflicts = self.update(docs)
        if conflicts:
            return conflicts
        self.commit()

    def update(self, docs=None):
        if docs is None:
            request = self._get_request_base_doc()
            request['process'] = UPDATE_PROCESS
            response = self._send(request)
            self.session_id = response['session_id']
            docs = [Document(**doc) for doc in response['docs']]
        docs_inspected = self.inspect_conflicts(docs)
        if docs_inspected['conflict_detected']:
            return docs_inspected
        ids = self._update(docs, UPDATE_PROCESS)
        self.db.save_last_sync(ids, UPDATE_PROCESS)

    def commit(self):
        request = self._get_request_base_doc()
        request['session_id'] = self.session_id
        request['process'] = COMMIT_PROCESS
        request['docs'] = self.db.get_docs_to_commit()
        ids = []
        if request['docs']:
            response = self._send(request)
            docs = [Document(**doc) for doc in response['docs']]
            ids = self._update(docs, COMMIT_PROCESS)
        self.db.save_last_sync(ids, COMMIT_PROCESS)

    def _update(self, docs, process):
        ids = []
        for doc in docs:
            doc = self.db.update(doc, process)
            if doc.id:
                ids.append(doc.id)
        return ids

    def inspect_conflicts(self, docs):
        docs_inspected = {'docs': [], 'conflict_detected': False}
        for remote_doc in docs:
            try:
                local_doc = self.db.get(remote_doc.sid, pk='sid')
            except NotFoundError:
                local_doc = None
            if local_doc and not local_doc.synced and not remote_doc.merged():
                docs_inspected['conflict_detected'] = True
                inspected = {'conflict': True,
                             'remote_doc': remote_doc,
                             'local_doc': local_doc,
                             'ok_doc': None}
            else:
                inspected = {'conflict': False,
                             'remote_doc': None,
                             'local_doc': None,
                             'ok_doc': remote_doc}
            docs_inspected['docs'].append(inspected)
        return docs_inspected

    def _get_request_base_doc(self):
        return {'user'      : config.USER,
                'key_name'  : config.KEY_NAME,
                'session_id': None,
                'process'   : None,
                'value'     : None,
                'last_tid'  : self.db.get_last_tid(),
                'docs'      : []}

    def get(self, id):
        return self.db.get(id)

    def server_get(self, sid):
        request = self._get_request_base_doc()
        request['process'] = 'get'
        request['value'] = sid
        response = self._send(request)
        if len(response['docs']) == 1:
            doc = Document(**response['docs'][0])
            return doc

    def getall(self):
        return self.db.getall()

    def save(self, doc):
        return self.db.save(doc)

    def delete(self, doc):
        return self.db.delete(doc)

    def search(self, regex):
        return self.db.search(regex)

    def server_search(self, regex):
        request = self._get_request_base_doc()
        request['process'] = 'search'
        request['value'] = regex
        response = self._send(request)
        docs = []
        for doc in response['docs']:
            docs.append(Document(**doc))
        return docs

    def status(self):
        return self.db.status()

    def _send(self, request):
        msg  = json.dumps(request)
        enc  = crypto.encrypt(msg, config.SERVER_PUB_KEY)
        data = base64.b64encode(enc)

        url = self._get_url(request)
        data = self.fetch(url, data)

        enc = base64.b64decode(data)
        msg = crypto.decrypt(enc, CLIENT_PRV_KEY)
        response = json.loads(msg)
        return response

    def _get_url(self, request):
        args = (config.SERVER_ADDR, config.SERVER_PORT,
                request['process'], request['user'])
        url = 'http://%s:%s/%s?user=%s' % args
        return url

    def fetch(self, url, data=None):
        if data is not None:
            data = urllib.urlencode({'data': data})
            req = urllib2.Request(url, data)
        else:
            req = url
        res = urllib2.urlopen(req)
        return res.read()

    def send_to_gist(self, doc):
        if config.GITHUB_USER and config.GITHUB_PASSWORD:
            from lai.lib import gist
            g = gist.Gist(config.GITHUB_USER, config.GITHUB_PASSWORD)
            return g.create(True, doc)
        else:
            return "Github credentials not configured."

if __name__ == '__main__':
    from lai.database import Database
    database = Database()
    client = Client(database)
    docs = client.search('awk')
    for doc in docs:
        print doc
