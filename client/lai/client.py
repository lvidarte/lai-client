# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import json
import pymongo

from pprint import pprint

try:
    from bson.objectid import ObjectId
except ImportError:
    from pymongo.objectid import ObjectId

import config


conn = pymongo.Connection(config.DB_HOST, config.DB_PORT)
db   = conn[config.DB_NAME]
coll = db[config.DB_COLLECTION]


def get(*args):
    params = {'_id': ObjectId(args[0])} if len(args) else {}
    docs = coll.find(params)
    fmt = "%-24s %-20s %-5s %-5s %-24s %-5s"
    print fmt % ('_id', 'data', 'ci', 'del', 'sid', 'tid')
    for doc in docs:
        print fmt % (doc['_id'], doc['data'], doc.get('commit'),
                     doc.get('deleted'), doc.get('server_id'),
                     doc.get('transaction_id'))


def add(*args):
    doc = {'data': args[0], 'commit': True}
    return coll.insert(doc)


def update(*args):
    _id = ObjectId(args[0])
    data = args[1]
    return coll.update({'_id': _id},
                       {'$set': {'data': data, 'commit': True}})


def delete(*args):
    _id = ObjectId(args[0])
    doc = list(coll.find({'_id': _id}))[0]
    if 'server_id' in doc:
        coll.update({'_id': _id},
                    {'$set': {'deleted': True, 'commit': True}})
    else:
        coll.remove({'_id': _id})


def up(*args):
    tid = args[0] if len(args) else get_last_transaction_id()
    url = "%s/%s" % (config.SERVER, tid)
    req = urllib2.urlopen(url)
    data = json.loads(req.read())
    if len(data['docs']):
        for doc in data['docs']:
            process_update(doc)
        return "updated ok"
    else:
        return "nothing to update"


def process_update(doc):
    if doc['deleted']:
        coll.remove({'server_id': doc['server_id']})
    else:
        coll.update({'server_id': doc['server_id']},
                    {'$set': {'transaction_id': doc['transaction_id'],
                              'data': doc['data']}},
                    safe=True, upsert=True)


def ci():
    url = "%s/%s" % (config.SERVER, get_last_transaction_id())

    docs = []
    for doc in coll.find({'commit': True}):
        docs.append(get_doc_for_commit(doc))

    if len(docs):
        data = urllib.urlencode({'docs': json.dumps(docs)})
        req = urllib2.Request(url, data)
        res = urllib2.urlopen(req)
        data = json.loads(res.read())

        if 'error' in data:
            return data['error']
        else:
            for doc in data['docs']:
                process_commit(doc)
            return "%d docs commited" % len(data['docs'])
    else:
        return "nothing to commit"


def process_commit(doc):
    _id = ObjectId(doc['client_id'])
    if 'deleted' in doc and doc['deleted']:
        coll.remove({'_id': _id})
    else:
        coll.update({'_id': _id},
                    {'$set': {'server_id': doc['server_id'],
                              'transaction_id': doc['transaction_id'],
                              'commit': False}})

def get_last_transaction_id():
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
            pprint(rs)
        except KeyError, e:
            print "Method not implemented"
            print e
    else:
        print "Usage: lai METHOD [arg1 [, argn]]"
