# -*- coding: utf-8 -*-


class Database(object):
    """Factory"""

    def __new__(cls, engine=None, config=None):
        if engine == 'sqlite':
            from lai.db import DBSqlite
            return DBSqlite(config)
        else:
            raise Exception('Invalid engine %s. Valids: %s' % (engine, ENGINES.keys()))
