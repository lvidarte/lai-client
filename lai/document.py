

class Document(object):

    VALID_ATTRS = ('id', 'sid', 'tid', 'public', 'synced', 'data')

    def __init__(self, data=None, id=None, sid=None, tid=None,
                 public=False, synced=False):
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
