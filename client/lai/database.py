# -*- coding: utf-8 -*-

import pymongo

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId

import config


class DatabaseBase(object):
    """Abstract class"""

    def connect(self):
        raise NotImplementedError('connect not implemented')

    def search(self, regex):
        raise NotImplementedError('search not implemented')

    def __str__(self):
        raise NotImplementedError('__str__ not implemented')


class DatabaseMongo(DatabaseBase):

    def __init__(self, host=None, port=None, name=None, collection=None):
        self.host = host or config.DB_HOST
        self.port = port or config.DB_PORT
        self.name = name or config.DB_NAME
        self.collection = collection or config.DB_COLLECTION
        self.connect()

    def connect(self):
        self.connection = pymongo.Connection(self.host, self.port)
        self.db = self.connection[self.name]
        self.coll = self.db[self.collection]

    def search(self, regex):
        return list(self.coll.find({'data': {'$regex': regex}}))

    def __str__(self):
        return "mongodb://%s:%s/%s?%s" % (self.host, self.port,
                                          self.name, self.collection)


class DatabaseMySQL(DatabaseBase):
    pass


ENGINES = {'mongodb': DatabaseMongo,
           'mysql'  : DatabaseMySQL,}


class Database(object):

    """Factory class"""
    def __new__(cls, engine=None, *args, **kwargs):
        try:
            return ENGINES[engine or config.DB_ENGINE](*args, **kwargs)
        except KeyError:
            raise Exception('Invalid engine')



if __name__ == '__main__':
    database = Database('mongodb')
    for doc in database.search(''):
        print doc
