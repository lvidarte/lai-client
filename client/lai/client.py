# -*- coding: utf-8 -*-

## tid = transaction_id

import sys
import urllib
import urllib2
import json
import pymongo

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId


from lai import config


conn = pymongo.Connection(config.DB_HOST, config.DB_PORT)
db = conn[config.DB_NAME]
coll = db[config.DB_COLLECTION]


def get(*args):
    params = json.loads(args[0]) if len(args) else {}
    if '_id' in params:
        params['_id'] = ObjectId(params['_id'])
    return list(coll.find(params))


def add(*args):
    doc = {'data': args[0],
           'commit': True}
    return coll.insert(doc)


def update(*args):
    _id = args[0]
    data = args[1]
    return coll.update({'_id': ObjectId(_id)}, {'$set': {'data': data, 'commit': True}})


def delete(*args):
    return coll.remove({'_id': ObjectId(args[0])})


def up():
    tid = get_max_transaction_id()
    url = "%s/%s" % (config.SERVER, tid)
    req = urllib2.urlopen(url)
    docs = json.loads(req.read())
    if len(docs):
        for doc in docs:
            coll.update({'server_id': doc['server_id']},
                        {'$set': {'transaction_id': doc['transaction_id'],
                                  'data': doc['data']}},
                        safe=True, upsert=True)
        return "updated ok"
    else:
        return "nothing to update"


def ci():
    tid = get_max_transaction_id()
    url = "%s/%s" % (config.SERVER, tid)

    docs = []
    for doc in coll.find({'commit': True}):
        docs.append(get_doc_for_commit(doc))

    data = urllib.urlencode({'docs': json.dumps(docs)})
    req = urllib2.Request(url, data)
    res = urllib2.urlopen(req)

    for doc in json.loads(res.read()):
        coll.update({'_id': ObjectId(doc['client_id'])},
                    {'$set': {'server_id': doc['server_id'],
                              'transaction_id': doc['transaction_id'],
                              'commit': False}})


def get_max_transaction_id():
    try:
        docs = coll.find({'transaction_id': {'$gt': 0}})
        docs = docs.sort('transaction_id', -1).limit(1)
        return int(docs.next()['transaction_id'])
    except StopIteration:
        return 0


def get_doc_for_commit(doc):
    _doc = {'client_id': str(doc['_id']), 'data': doc['data']}
    if doc.get('server_id'):
        _doc['server_id'] = doc['server_id']
        _doc['transaction_id'] = doc['transaction_id']
    if doc.get('deleted'):
        _doc['deleted'] = doc['deleted']
    return _doc


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            if len(sys.argv) > 2:
                rs = globals()[sys.argv[1]](*sys.argv[2:])
            else:
                rs = globals()[sys.argv[1]]()
            print rs
        except KeyError, e:
            print "Method not implemented"
            print e
    else:
        print "Usage: lai METHOD [arg1 [, argn]]"
