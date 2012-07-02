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
        handlers = [(r'/(\w+)/(\d+)', MainHandler)]
        self.conn = pymongo.Connection(options.db_host, options.db_port)
        self.db = self.conn[options.db_name]
        super(Application, self).__init__(handlers, debug=True)

class MainHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(MainHandler, self).__init__(*args, **kwargs)
        self.coll = self.application.db[options.db_collection]
        self.set_header('Content-Type', 'application/json')

    def get(self, user, tid):
        tid = int(tid)
        docs = self._get_update_docs(user, tid)
        self.write(json.dumps({'docs': docs}))

    def _get_update_docs(self, user, tid):
        docs = []
        cur = self.coll.find({'tid': {'$gt': tid},
                              '$or': [{'users':    {'$in': [user]}},
                                      {'usersdel': {'$in': [user]}}]
                             })

        for doc in cur:
            _doc = {'sid'     : str(doc['_id']),
                    'tid'     : doc['tid'],
                    'data'    : doc['data'],
                    'keys'    : doc['keys'],
                    'users'   : doc['users'],
                    'usersdel': doc['usersdel']}
            docs.append(_doc)
        return docs

    def post(self, user, tid):
        tid = int(tid)
        docs = json.loads(self.get_argument('docs'))
        if len(self._get_update_docs(user, tid)) == 0:
            tid = self._get_next_tid()
            _docs = []
            for doc in docs:
                _doc = self._process(doc, tid)
                _docs.append(_doc)
            self.write(json.dumps({'docs': _docs}))
        else:
            self.write(json.dumps({'error': 'you must update first'}))

    def _get_next_tid(self):
        query = {'_id': options.db_collection}
        update = {'$inc': {'last_tid': 1}}
        collection = self.application.db['counter']
        row = collection.find_and_modify(query, update, upsert=True, new=True)
        return row['last_tid']

    def _process(self, doc, tid):
        _doc = {'tid'     : tid,
                'data'    : doc['data'],
                'keys'    : doc['keys'],
                'users'   : doc['users'],
                'usersdel': doc['usersdel']}

        if doc['sid'] is not None:
            _id  = ObjectId(doc['sid'])
            self.coll.update({'_id': _id}, {'$set': _doc})
        else:
            _id  = self.coll.insert(_doc)

        _doc = {'id'      : doc['id'],
                'sid'     : str(_id),
                'tid'     : tid,
                'users'   : doc['users'],
                'usersdel': doc['usersdel']}
        return _doc


if __name__ == '__main__':
    tornado.options.parse_config_file('lai/config.py')
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port)
    logging.info('lai server started')
    tornado.ioloop.IOLoop.instance().start()

