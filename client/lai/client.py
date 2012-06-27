# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

from lai import config
from lai.document import Document
from lai.database import UPDATE_RESPONSE, COMMIT_RESPONSE


class Client:

    def __init__(self, database):
        self.db = database

    def update(self):
        data = self.fetch()
        if len(data['docs']):
            for doc_ in data['docs']:
                doc = Document(**doc_)
                self.db.update(doc, type=UPDATE_RESPONSE)
            return 'ok'
        else:
            return 'nothing to update'

    def commit(self):
        docs = self.db.get_docs_for_commit()
        if len(docs):
            data = self.fetch(docs)
            if 'error' in data:
                return data['error']
            else:
                for doc_ in data['docs']:
                    doc = Document(**doc_)
                    self.db.update(doc, type=COMMIT_RESPONSE)
                return 'ok'
        else:
            return 'nothing to commit'

    def get(self, id):
        return self.db.get(id)

    def save(self, document):
        return self.db.save(document)

    def delete(self):
        return self.db.delete(document)

    def search(self, regex):
        return self.db.search(regex)

    def fetch(self, docs=None):
        url = self.get_request_url()
        if docs is not None:
            data = urllib.urlencode({'docs': json.dumps(docs)})
            req = urllib2.Request(url, data)
        else:
            req = url
        res= urllib2.urlopen(req)
        return json.loads(res.read())

    def get_request_url(self):
        tid = self.db.get_last_tid()
        return "%s/%s/%s" % (config.SERVER, config.USER, tid)


if __name__ == '__main__':
    from lai import Database
    database = Database()
    client = Client(database)
    docs = client.search('')
    for doc in docs:
        print doc
