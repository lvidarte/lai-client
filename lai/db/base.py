# -*- coding: utf-8 -*-

class DBBase(object):

    def __init__(self, config):
        self.config = config

    def connect(self):
        raise NotImplementedError('connect not implemented')

    def get_last_tid(self):
        raise NotImplementedError('get_last_tid not implemented')

    def get(self, doc):
        raise NotImplementedError('get not implemented')

    def save(self, doc):
        raise NotImplementedError('save not implemented')

    def update(self, doc):
        raise NotImplementedError('save not implemented')

    def search(self, regex):
        raise NotImplementedError('search not implemented')

    def status(self):
        raise NotImplementedError('status not implemented')

    def __str__(self):
        raise NotImplementedError('__str__ not implemented')
