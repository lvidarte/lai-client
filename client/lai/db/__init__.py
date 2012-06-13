from db.sqlite import DBSqlite

class DBBase(object):

    def __init__(self, config):
        self._config = config
        self.connect()

    def connect(self):
        raise NotImplementedError('connect not implemented')

    def search(self, regex):
        raise NotImplementedError('search not implemented')

    def __str__(self):
        return "Database Base"
