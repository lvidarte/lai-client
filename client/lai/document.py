# -*- coding: utf-8 -*-

import string
from lai import config


class Document:

    VALID_ATTRS = ('data', 'keys', 'id', 'sid', 'tid',
                   'users', 'usersdel', 'synched')

    def __init__(self, data=None, keys=None, id=None, sid=None,
                 tid=None, users=[], usersdel=[], synched=False):
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
        if user in self.users:
            del self.users[self.users.index(user)]
            if user not in self.usersdel:
                self.usersdel.append(user)

    def set_keys(self, data=None):
        if data is None:
            data = self.data
        if data is not None:
            self.keys = self.get_keys(data)

    def get_keys(self, data):
        words = []
        for line in data.splitlines():
            for word in self._get_words(line):
                if self._is_valid(word) and word not in words:
                    words.append(word)
        return ' '.join(sorted(words))

    def _get_words(self, line):
        chars = []
        for char in line:
            if char in string.punctuation:
                chars.append(' ')
            else:
                chars.append(char)
        return ''.join(chars).split()

    def _is_valid(self, word):
        if len(word) < 2:
            return False
        if word.isdigit():
            return False
        if word in self._get_stop_words():
            return False
        return True

    def _get_stop_words(self):
        return ['de', 'la', 'el', 'lo']

    def __repr__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    doc = Document('Lorem ipsum dolor sit amet.', keys='lorem ipsum amet')
    print doc
