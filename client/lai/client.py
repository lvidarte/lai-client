# -*- coding: utf-8 -*-

from lai import config


class Client:

    def __init__(self, database):
        self.db = database

    def update(self):
        pass

    def commit(self):
        pass

    def save(self, document):
        return self.db.save(document)

    def delete(self):
        pass

    def search(self, regex):
        return self.db.search(regex)

    def fetch(self, data=None):
        #url = self.get_url()
        #if data is not None:
            #POST
        #else:
            #GET
        #return json.loads(data)
        pass

    def get_url(self):
        tid = self.db.get_last_tid()
        return "%s/%s/%s" % (config.SERVER, config.USER, tid)


if __name__ == '__main__':
    from lai import Database
    config = {'HOST': 'localhost',
              'PORT': 27017,
              'NAME': 'lai',
              'TABLE': 'test'}
    database = Database('mongo', config)
    client = Client(database)
    docs = client.search('')
    for doc in docs:
        print doc
