import pymongo
from base import DatabaseBase

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId

class DatabaseMongo(DatabaseBase):

    #engine = "mongo"

    def connect(self): 
        self.host  = self._config.DB_HOST
        self.port  = self._config.DB_PORT
        self.name  = self._config.DB_NAME
        self.table = self._config.DB_TABLE

        self.connection = pymongo.Connection(self.host, self.port)
        self.db = self.connection[self.name]
        self.collection = self.db[self.table]

    def search(self, regex):
        return list(self.collection.find({'data': {'$regex': regex}}))


