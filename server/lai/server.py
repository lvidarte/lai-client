import tornado.ioloop
import tornado.web
import json
import pymongo

conn = pymongo.Connection()
db = conn.lai

class MainHandler(tornado.web.RequestHandler):
    def get(self, oid=0):
        docs = []
        for doc in db.docs.find({'oid': {'$gt': oid}}):
            docs.append(doc)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(docs))

    def post(self):
        docs = json.loads(self.get_argument('docs'))
        oid = self._get_max_oid(docs)
        if self._check_db_oid(oid):
            docs_ = [{'oid': oid}]
            for doc in docs:
                docs_.append(self._process(doc))
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(docs_))

    def _process(self, doc):
        return {'doc': doc}

    def _get_max_oid(self, docs):
        return max(docs, key=lambda doc:doc['oid'])['oid']

    def _check_db_oid(self, oid):
        return not db.docs.find({'oid': {'$gt': oid}}).count()


if __name__ == '__main__':
    application = tornado.web.Application([
            (r'/', MainHandler),
            (r'/(\d+)?', MainHandler),
        ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
