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
from lai.database import DatabaseException, UPDATE_PROCESS, COMMIT_PROCESS
from lai.lib import crypto
#from lai.lib import gist


CLIENT_PRV_KEY = open(config.CLIENT_PRV_KEY_PATH, 'r').read()


class Client:

    def __init__(self, database):
        self.db = database
        self.db.connect()

    def sync(self):
        # Update
        request = self._get_request_base_doc()
        request['process'] = UPDATE_PROCESS
        response = self._send(request)
        ids = self._update(response)
        self.db.save_last_sync(UPDATE_PROCESS, ids)
        # Commit
        request = self._get_request_base_doc()
        request['session_id'] = response['session_id']
        request['process'] = COMMIT_PROCESS
        request['docs'] = self.db.get_docs_to_commit()
        ids = []
        if len(request['docs']):
            response = self._send(request)
            ids = self._update(response)
        self.db.save_last_sync(COMMIT_PROCESS, ids)

    def _update(self, response):
        ids = []
        if len(response['docs']):
            for doc_ in response['docs']:
                doc = Document(**doc_)
                doc = self.db.update(doc, type=response['process'])
                ids.append(doc.id)
        return ids

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

#   def send_to_gist(self, doc):
#       g = gist.Gist(config.GITHUB_USER, config.GITHUB_PASSWORD)
#       return g.create(True, doc)

if __name__ == '__main__':
    from lai.database import Database
    database = Database()
    client = Client(database)
    docs = client.search('awk')
    for doc in docs:
        print doc
