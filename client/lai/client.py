# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

from lai import config


class Client:

    def __init__(self, database):
        self.db = database

    def update(self):
        data = self.fetch()
        if len(data['docs']):
            for doc in data['docs']:
                self.db.update(doc, synched=True, pk='sid')
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
                for doc in data['docs']:
                    self.db.update(doc, synched=True)
                return 'ok'
        else:
            return 'nothing to commit'

    def get(self, id):
        return self.db.get(id)

    def save(self, document):
        return self.db.save(document)

    def delete(self):
        pass

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
