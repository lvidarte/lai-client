from lai.config import DATABASE


UPDATE_PROCESS = 'update'
COMMIT_PROCESS = 'commit'


class DatabaseException(Exception):
    pass


class Database(object):
    """Factory"""

    def __new__(cls, engine=None, config=None):
        if engine is None:
            engine = DATABASE['ENGINE']
        if config is None:
            config = DATABASE

        if engine == 'sqlite':
            from lai.db import DBSqlite
            return DBSqlite(config)
        if engine == 'mongo':
            from lai.db import DBMongo
            return DBMongo(config)
        else:
            raise Exception('Invalid engine ' + engine)

