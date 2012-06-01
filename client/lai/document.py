# -*- coding: utf-8 -*-

from data import Data


class Document:

    def __init__(self, data, id=None, tid=None,
                 sid=None, synched=True, keys=None,
                 users=None, usersdel=None):
        self.data = Data(data)
        self.id = id
        self.tid = tid
        self.sid = sid
        self.synched = synched
        self.keys = keys or ''
        self.users = users or []
        self.usersdel = usersdel or []

    def get_dict(self):
        return {
           'id'      : self.id,
           'sid'     : self.sid,
           'tid'     : self.tid,
           'data'    : self.data,
           'keys'    : self.keys,
           'synched' : self.synched,
           'users'   : self.users,
           'usersdel': self.usersdel,
        }


if __name__ == '__main__':
    doc = Document('{"x": 0, "y": 1}')
    print doc.data.dumps()
