# -*- coding: utf-8 -*-

from lai import config


class Document:

    VALID_ATTRS = ('id', 'sid', 'tid', 'user',
                   'public', 'synced', 'data')

    def __init__(self, data=None, id=None, sid=None, tid=None,
                 user=None, public=False, synced=False):
        if user is None:
            user = config.USER
        self.from_dict(locals())

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

    def __repr__(self):
        return ', '.join(["%s=%s" % (key, self.__dict__[key])
                          for key in self.VALID_ATTRS])


if __name__ == '__main__':
    doc = Document('Lorem ipsum dolor sit amet.')
    print doc
    doc = Document(dict(x=0, y=1))
    print doc
