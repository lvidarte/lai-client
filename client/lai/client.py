# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

from lai import config
from lai.document import Document
from lai.database import DatabaseException, UPDATE_RESPONSE, COMMIT_RESPONSE

class ClientException(Exception):
    pass

class Client:

    def __init__(self, database):
        self.db = database

        try:
            self.db.connect()
        except DatabaseException as e:
            raise ClientException(e)

    def update(self):

        try:
            data = self.fetch()
        except urllib2.URLError:
            return 'http connection error'

        if len(data['docs']):
            for doc_ in data['docs']:
                doc = Document(**doc_)

                try: 
                    self.db.update(doc, type=UPDATE_RESPONSE)
                except DatabaseException as e:
                    raise ClientException(e)
            return 'ok'
        else:
            return 'nothing to update'

    def commit(self):
        try:
            docs = self.db.get_docs_for_commit()
        except DatabaseException as e:
            raise ClientException(e)

        if len(docs):
            try:
                data = self.fetch(docs)
            except urllib2.URLError:
                ClientException('http connection error')

            if 'error' in data:
                return data['error']
            else:
                for doc_ in data['docs']:
                    doc = Document(**doc_)

                    try:
                        self.db.update(doc, type=COMMIT_RESPONSE)
                    except DatabaseException as e:
                        raise ClientException(e)

                return 'ok'
        else:
            return 'nothing to commit'

    def get(self, id):
        return self.db.get(id)

    def save(self, doc):
        if doc.keys is None:
            doc.set_keys()
        try:
            doc = self.db.save(doc)
        except DatabaseException as e:
            raise ClientException(e)
        else:
            return doc

    def delete(self, doc):
        return self.db.delete(doc)

    def search(self, regex):
        return self.db.search(regex)

    def status(self):
        return self.db.status()

    def fetch(self, docs=None):
        url = self.get_request_url()
        if docs is not None:
            data = urllib.urlencode({'docs': json.dumps(docs)})
            req = urllib2.Request(url, data)
        else:
            req = url
        res = urllib2.urlopen(req)
        return json.loads(res.read())

    def get_request_url(self):
        tid = self.db.get_last_tid()
        return "%s/%s/%s" % (config.SERVER, config.USER, tid)


if __name__ == '__main__':
    from lai.database import Database
    database = Database()
    client = Client(database)
    docs = client.search('awk')
    for doc in docs:
        print doc
