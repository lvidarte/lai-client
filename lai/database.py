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

