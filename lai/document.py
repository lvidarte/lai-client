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
from lai.data import Data

import json


class Document(dict):

    VALID_ATTRS = ('id', 'sid', 'tid', 'user', 'public', 'synced', 'data')

    def __init__(self, data=None, id=None, sid=None, tid=None,
                 user=None, public=False, synced=False):
        self.__setitem__('data', data)
        self.__setitem__('id', id)
        self.__setitem__('sid', sid)
        self.__setitem__('tid', tid)
        if user is None:
            user = config.USER
        self.__setitem__('user', user)
        self.__setitem__('public', bool(public))
        self.__setitem__('synced', bool(synced))

    def __getattr__(self, attr):
        return self.get(attr, None)

    def __setitem__(self, key, value):
        if key in self.VALID_ATTRS:
            if key == 'data' and (value is not None and type(value) != Data):
                if type(value) == dict:
                    value = Data(**value)
                elif type(value) in (str, unicode):
                    try:
                        d = json.loads(value)
                        value = Data(**d)
                    except ValueError:
                        value = Data(value)
                else:
                    value = Data(value)
            super(Document, self).__setitem__(key, value)

    __setattr__ = __setitem__
    __delattr__ = dict.__delitem__


if __name__ == '__main__':
    doc = Document('Lorem ipsum dolor sit amet.')
    print doc
    doc = Document(dict(x=0, y=1))
    print doc
