# -*- coding: utf-8 -*-

import pymongo

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId

import config


class Database:
    conn = pymongo.Connection(config.DB_HOST, config.DB_PORT)
    db   = conn[config.DB_NAME]
    coll = db[config.DB_COLLECTION]

    @classmethod
    def search(cls, regex):
        return cls.coll.find({'data': {'$regex': regex}})


if __name__ == '__main__':
    for doc in Database.search(''):
        print doc
