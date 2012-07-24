# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

from lai import config
#from lai.gist import Gist, GistException
from lai.document import Document
from lai.database import DatabaseException, UPDATE_RESPONSE, COMMIT_RESPONSE


class ClientException(Exception):
    pass


class Client:

    def __init__(self, database):
        try:
            self.db = database
            self.db.connect()
        except DatabaseException as e:
            raise ClientException(e)

    def sync(self):
        pass

    def update(self):
        try:
            data = self.fetch()
        except urllib2.URLError as e:
            raise ClientException(e)
        if len(data['docs']):
            for doc_ in data['docs']:
                doc = Document(**doc_)
                try: 
                    self.db.update(doc, type=UPDATE_RESPONSE)
                except DatabaseException as e:
                    raise ClientException(e)
            return len(data['docs'])

    def commit(self):
        try:
            docs = self.db.get_docs_for_commit()
        except DatabaseException as e:
            raise ClientException(e)
        if len(docs):
            try:
                data = self.fetch(docs)
            except urllib2.URLError as e:
                raise ClientException(e)
            if 'error' in data:
                raise ClientException(data['error'])
            else:
                for doc_ in data['docs']:
                    try:
                        doc = Document(**doc_)
                        self.db.update(doc, type=COMMIT_RESPONSE)
                    except DatabaseException as e:
                        raise ClientException(e)
                return len(data['docs'])

    def get(self, id):
        try:
            return self.db.get(id)
        except DatabaseException as e:
            raise ClientException(e)

    def getall(self):
        try:
            return self.db.getall()
        except DatabaseException as e:
            raise ClientException(e)

    def save(self, doc):
        try:
            doc = self.db.save(doc)
        except DatabaseException as e:
            raise ClientException(e)
        return doc

    def delete(self, doc):
        try:
            return self.db.delete(doc)
        except DatabaseException as e:
            raise ClientException(e)

    def search(self, regex):
        try:
            return self.db.search(regex)
        except DatabaseException as e:
            raise ClientException(e)

#   def status(self):
#       try:
#           return self.db.status()
#       except DatabaseException as e:
            raise ClientException(e)

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

#   def send_to_gist(self, doc):
#       try:
#           g = Gist(config.GITHUB_USER, config.GITHUB_PASSWORD)
#           return g.create(True, doc)
#       except GistException as e:
#           raise ClientException(e)

if __name__ == '__main__':
    from lai.database import Database
    database = Database()
    client = Client(database)
    docs = client.search('awk')
    for doc in docs:
        print doc
