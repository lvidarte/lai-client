# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import options

import json
import pymongo
import logging

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/(\d+)?', MainHandler)]
        self.conn = pymongo.Connection(options.db_host, options.db_port)
        self.db = self.conn[options.db_name]
        super(Application, self).__init__(handlers, debug=True)

class MainHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(MainHandler, self).__init__(*args, **kwargs)
        self.coll = self.application.db[options.db_collection]
        self.set_header('Content-Type', 'application/json')

    def get(self, tid=None):
        tid = self._check_tid(tid)
        docs = self._get_update_docs(tid)
        self.write(json.dumps({'docs': docs}))

    def _get_update_docs(self, tid):
        docs = []
        params = {'transaction_id': {'$gt': tid}}
#       if tid == 0:
#           params['deleted'] = {'$ne': True}
        for doc in self.coll.find(params):
            _doc = {'server_id':      str(doc['_id']),
                    'transaction_id': doc['transaction_id'],
                    'data':           doc['data'],
                    'deleted':        doc.get('deleted', False)}
            docs.append(_doc)
        return docs

    def post(self, tid=None):
        tid = self._check_tid(tid)
        docs = json.loads(self.get_argument('docs'))
        if len(self._get_update_docs(tid)) == 0:
            tid += 1
            _docs = []
            for doc in docs:
                _doc = self._process(doc, tid)
                _docs.append(_doc)
            self.write(json.dumps({'docs': _docs}))
        else:
            self.write(json.dumps({'error': 'you must update first'}))

    def _process(self, doc, transaction_id):
        _doc = {'transaction_id': transaction_id, 'data': doc['data']}

        # Update/Delete
        if 'server_id' in doc:
            if 'deleted' in doc:
                _doc['deleted'] = True
            _id  = ObjectId(doc['server_id'])
            self.coll.update({'_id': _id}, {'$set': _doc})
        # Insert
        else:
            _id  = self.coll.insert(_doc)

        _doc = {'server_id':      str(_id),
                'client_id':      doc['client_id'],
                'transaction_id': transaction_id}
        if 'deleted' in doc:
            _doc['deleted'] = True
        return _doc

#   def _get_last_tid(self, docs):
#       return max(docs, key=lambda doc:doc['tid'])['tid']

#   def _check_db_tid(self, tid):
#       return not self.coll.find({'transaction_id': {'$gt': tid}}).count()

    def _check_tid(self, tid):
        return 0 if tid is None else int(tid)


if __name__ == '__main__':
    tornado.options.parse_config_file('lai/config.py')
    tornado.options.parse_command_line()

    application = Application()
    application.listen(options.port)

    logging.info('lai server started')
    tornado.ioloop.IOLoop.instance().start()

