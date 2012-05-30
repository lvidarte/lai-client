# -*- coding: utf-8 -*-


class Client:

    def __init__(self, database):
        self.db = database

    def update(self):
        pass

    def commit(self):
        pass

    def save(self):
        pass

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


if __name__ == '__main__':
    from lai import Database
    client = Client(Database())
    docs = client.search('')
    for doc in docs:
        print doc
