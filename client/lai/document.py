# -*- coding: utf-8 -*-

from lai import config


class Document:

    users = []
    usersdel = []

    def __init__(self, data=None, id=None, sid=None, tid=None,
                 keys=None, users=None, usersdel=None):
        self.data = data
        self.keys = keys
        self.id  = id
        self.sid = sid
        self.tid = tid
        if users is None and usersdel is None:
            self.add_user(config.USER)

    def set(self, data_dict):
        for key, value in data_dict.items():
            setattr(self, key, value)

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

    def __str__(self):
        return self.data


if __name__ == '__main__':
    doc = Document('Lorem ipsum dolor sit amet.', keys='lorem ipsum amet')
    print doc
