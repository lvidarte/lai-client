# -*- coding: utf-8 -*-

from database import Database


class Client:

    database = Database()

    @classmethod
    def update(cls):
        pass

    @classmethod
    def commit(cls):
        pass

    @classmethod
    def save(cls):
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def search(cls, regex):
        return cls.database.search(regex)

    def fetch(self, data=None):
        #url = self.get_url()
        #if data is not None:
            #POST
        #else:
            #GET
        #return json.loads(data)
        pass


if __name__ == '__main__':
    docs = Client.search('')
    for doc in docs:
        print doc
