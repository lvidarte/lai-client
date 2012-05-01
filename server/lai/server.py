# -*- coding: utf-8 -*-

## tid = transaction_id

import tornado.ioloop
import tornado.web
import json
import pymongo

conn = pymongo.Connection()
db = conn.lai


class MainHandler(tornado.web.RequestHandler):
    def get(self, tid=None):
        tid = self._check_tid(tid)
        docs = []
        for doc in db.docs.find({'tid': {'$gt': tid}}):
            doc['_id'] = str(doc['_id'])
            docs.append(doc)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(docs))

    def post(self, tid=None):
        tid = self._check_tid(tid)
        docs = json.loads(self.get_argument('docs'))
        #tid = self._get_max_tid(docs)
        if self._check_db_tid(tid):
            tid += 1
            docs_ = []
            for doc in docs:
                docs_.append(self._process(doc, tid))
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(docs_))
        else:
            self.write('you must update first')

    def _process(self, doc, tid):
        doc['tid'] = tid
        doc['_id'] = str(db.docs.insert(doc))
        del doc['data']
        return doc

    def _get_max_tid(self, docs):
        return max(docs, key=lambda doc:doc['tid'])['tid']

    def _check_db_tid(self, tid):
        return not db.docs.find({'tid': {'$gt': tid}}).count()

    def _check_tid(self, tid):
        return 0 if tid is None else int(tid)


if __name__ == '__main__':
    application = tornado.web.Application([
            (r'/(\d+)?', MainHandler),
        ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
