# -*- coding: utf-8 -*-

# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

from lai import config


UPDATE_PROCESS = 'update'
COMMIT_PROCESS = 'commit'


class DatabaseException(Exception):
    pass


class NotFoundError(DatabaseException):
    pass


class Database(object):
    """Factory"""

    def __new__(cls, **kwargs):

        try:
            engine = kwargs['engine']
            del kwargs['engine']
        except KeyError:
            raise Exception('Engine not set')

        if engine == 'sqlite':
            from lai.db.sqlite import DBSqlite
            return DBSqlite(**kwargs)
        if engine == 'mongo':
            from lai.db.mongo import DBMongo
            return DBMongo(**kwargs)
        if engine == 'mysql':
            from lai.db.mysql import DBMySQL
            return DBMySQL(**kwargs)
        else:
            raise Exception('Invalid engine ' + engine)

