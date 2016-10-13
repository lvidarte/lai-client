# -*- coding: utf-8 -*-

# Author: Leo Vidarte <http://nerdlabs.com.ar>
#
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

class DBBase(object):

    def connect(self):
        raise NotImplementedError('connect not implemented')

    def search(self, regex):
        raise NotImplementedError('search not implemented')

    def get(self, doc):
        raise NotImplementedError('get not implemented')

    def save(self, doc):
        raise NotImplementedError('save not implemented')

    def update(self, doc, process=None):
        raise NotImplementedError('update not implemented')

    def delete(self, doc):
        raise NotImplementedError('delete not implemented')

    def save_last_sync(self, ids, process):
        raise NotImplementedError('save_last_sync not implemented')

    def get_docs_to_commit(self):
        raise NotImplementedError('get_docs_to_commit not implemented')

    def get_last_tid(self):
        raise NotImplementedError('get_last_tid not implemented')

    def status(self):
        raise NotImplementedError('status not implemented')

    def __str__(self):
        raise NotImplementedError('__str__ not implemented')
