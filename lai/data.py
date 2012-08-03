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


class Data(dict):

    def __init__(self, body=None, help=None, *args, **kwargs):
        self.__setitem__('body', body)
        self.__setitem__('help', help)
        super(Data, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        return self.get(attr, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

