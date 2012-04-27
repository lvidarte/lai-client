import tornado.ioloop
import tornado.web
import json
import pymongo

conn = pymongo.Connection()
db = conn.lai


class MainHandler(tornado.web.RequestHandler):
    def get(self, oid=None):
        oid = self._check_oid(oid)
        docs = []
        for doc in db.docs.find({'oid': {'$gt': oid}}):
            doc['_id'] = str(doc['_id'])
            docs.append(doc)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(docs))

    def post(self, oid=None):
        oid = self._check_oid(oid)
        docs = json.loads(self.get_argument('docs'))
        #oid = self._get_max_oid(docs)
        if self._check_db_oid(oid):
            oid += 1
            docs_ = []
            for doc in docs:
                docs_.append(self._process(doc, oid))
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(docs_))
        else:
            self.write('you must update first')

    def _process(self, doc, oid):
        doc['oid'] = oid
        doc['_id'] = str(db.docs.insert(doc))
        del doc['data']
        return doc

    def _get_max_oid(self, docs):
        return max(docs, key=lambda doc:doc['oid'])['oid']

    def _check_db_oid(self, oid):
        return not db.docs.find({'oid': {'$gt': oid}}).count()

    def _check_oid(self, oid):
        return 0 if oid is None else int(oid)


if __name__ == '__main__':
    application = tornado.web.Application([
            (r'/(\d+)?', MainHandler),
        ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
