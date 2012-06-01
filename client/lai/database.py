# -*- coding: utf-8 -*-

import pymongo

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId

import config


class DatabaseBase(object):

    def __init__(self, host=None, port=None, name=None, table=None):
        self.host  = host  or config.DB_HOST
        self.port  = port  or config.DB_PORT
        self.name  = name  or config.DB_NAME
        self.table = table or config.DB_TABLE
        self.connect()

    def connect(self):
        raise NotImplementedError('connect not implemented')

    def search(self, regex):
        raise NotImplementedError('search not implemented')

    def __str__(self):
        return "%s://%s:%s/%s?%s" % (self.engine, self.host, self.port,
                                     self.name, self.table)


class DatabaseMongo(DatabaseBase):

    engine = "mongo"

    def connect(self):
        self.connection = pymongo.Connection(self.host, self.port)
        self.db = self.connection[self.name]
        self.collection = self.db[self.table]

    def search(self, regex):
        return list(self.collection.find({'data': {'$regex': regex}}))



class DatabaseMySQL(DatabaseBase):
    pass


ENGINES = {'mongo': DatabaseMongo,
           'mysql': DatabaseMySQL,}


class Database(object):
    """Factory class"""

    def __new__(cls, engine=None, *args, **kwargs):
        try:
            return ENGINES[engine or config.DB_ENGINE](*args, **kwargs)
        except KeyError:
            raise Exception('Invalid engine')



if __name__ == '__main__':
    database = Database('mongo')
    for doc in database.search(''):
        print doc
