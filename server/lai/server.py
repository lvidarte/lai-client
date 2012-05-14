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
        handlers = [(r'/(\d+)', MainHandler)]
        self.conn = pymongo.Connection(options.db_host, options.db_port)
        self.db = self.conn[options.db_name]
        super(Application, self).__init__(handlers, debug=True)

class MainHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(MainHandler, self).__init__(*args, **kwargs)
        self.coll = self.application.db[options.db_collection]
        self.set_header('Content-Type', 'application/json')

    def get(self, tid):
        tid = int(tid)
        docs = self._get_update_docs(tid)
        self.write(json.dumps({'docs': docs}))

    def _get_update_docs(self, tid):
        docs = []
        for doc in self.coll.find({'tid': {'$gt': tid}}):
            _doc = {'sid':  str(doc['_id']),
                    'tid':  doc['tid'],
                    'data': doc['data']}
            docs.append(_doc)
        return docs

    def post(self, tid):
        tid = int(tid)
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

    def _process(self, doc, tid):
        _doc = {'tid': tid, 'data': doc['data']}

        if 'sid' in doc:
            _id  = ObjectId(doc['sid'])
            self.coll.update({'_id': _id}, {'$set': _doc})
        else:
            _id  = self.coll.insert(_doc)

        _doc = {'sid':      str(_id),
                'cid':      doc['cid'],
                'tid': tid}
        return _doc

#   def _get_last_tid(self, docs):
#       return max(docs, key=lambda doc:doc['tid'])['tid']

#   def _check_db_tid(self, tid):
#       return not self.coll.find({'tid': {'$gt': tid}}).count()

#   def _get_tid(self, tid):
#       return 0 if tid is None else int(tid)


if __name__ == '__main__':
    tornado.options.parse_config_file('lai/config.py')
    tornado.options.parse_command_line()

    application = Application()
    application.listen(options.port)

    logging.info('lai server started')
    tornado.ioloop.IOLoop.instance().start()

