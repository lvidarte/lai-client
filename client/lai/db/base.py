# -*- coding: utf-8 -*-


class DBBase(object):

    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        raise NotImplementedError('connect not implemented')

    def search(self, regex):
        raise NotImplementedError('search not implemented')

    def __str__(self):
        raise NotImplementedError('__str__ not implemented')
