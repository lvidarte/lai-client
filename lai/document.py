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


class Document(object):

    VALID_ATTRS = ('id', 'sid', 'tid', 'user', 'public', 'synced', 'data')

    def __init__(self, data=None, id=None, sid=None, tid=None,
                 user=None, public=False, synced=False):
        if user is None:
            user = config.USER
        self._data = None
        self.from_dict(locals())

    def get_data(self):
        return self._data

    def set_data(self, value):
        if isinstance(value, (str, unicode)) and value.strip() == '':
            value = None
        if type(value) != dict and value is not None:
            value = {'body': value}
        self._data = value

    def del_data(self):
        self._data = None

    data = property(get_data, set_data, del_data)

    def from_dict(self, mapping):
        for key, value in mapping.items():
            if key in self.VALID_ATTRS:
                setattr(self, key, value)

    def to_dict(self):
        doc = {'data': self._data}
        for key, value in self.__dict__.items():
            if key in self.VALID_ATTRS:
                doc[key] = value
        return doc

    def __repr__(self):
        return str(self.to_dict())


if __name__ == '__main__':
    doc = Document('Lorem ipsum dolor sit amet.')
    print doc
    doc = Document(dict(x=0, y=1))
    print doc
