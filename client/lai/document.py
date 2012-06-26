# -*- coding: utf-8 -*-

from lai import config


class Document:

    VALID_ATTRS = ('data', 'keys', 'id', 'sid', 'tid',
                   'users', 'usersdel', 'synched')

    def __init__(self, data=None, keys=None, id=None, sid=None, tid=None,
                 users=[], usersdel=[], synched=False):
        self.from_dict(locals())
        if not users:
            self.add_user(config.USER)

    def from_dict(self, mapping):
        for key, value in mapping.items():
            if key in self.VALID_ATTRS:
                setattr(self, key, value)

    def to_dict(self):
        doc = {}
        for key, value in self.__dict__.items():
            if key in self.VALID_ATTRS:
                doc[key] = value
        return doc

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

    def __repr__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    doc = Document('Lorem ipsum dolor sit amet.', keys='lorem ipsum amet')
    print doc
