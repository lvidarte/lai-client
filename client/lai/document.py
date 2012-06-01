# -*- coding: utf-8 -*-

import json
import config
from data import Data


class Document:

    users = []
    usersdel = []

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


    """
    def __init__(self, data, key=None, id=None, sid=None, tid=None, synched=True,
                 keys=None, users=None, usersdel=None):
        self.data = Data(data, key)
        self.id   = id
        self.sid  = sid
        self.tid  = tid
        self.synched = synched
        if users is None and usersdel is None:
            self.add_user(config.USER)
    """

    def get_dict(self):
        return {
           'id'      : self.id,
           'sid'     : self.sid,
           'tid'     : self.tid,
           'data'    : self.data,
           'keys'    : self.data.keys,
           'synched' : self.synched,
           'users'   : self.users,
           'usersdel': self.usersdel,
        }

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)
        if user in self.usersdel:
            del self.usersdel[self.usersdel.index(user)]

    def del_user(self, user):
        if user not in self.usersdel:
            self.usersdel.append(user)
        if user in self.users:
            del self.users[self.users.index(user)]



if __name__ == '__main__':
    doc = Document('{"text": "Lorem ipsum dolor sit amet.", "value": 2}', key='text')
    print doc.get_dict()
