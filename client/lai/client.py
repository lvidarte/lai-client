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
    fmt = "%-24s %-24s %-5s %-5s %-20s"
    print fmt % ('_id', 'sid', 'tid', 'ci', 'data')
    for doc in docs:
        print fmt % (doc['_id'], doc['sid'], doc['tid'],
                     doc['commit'], doc['data'])
    return ''


def add(*args):
    docs = list(coll.find({'data': ''}).limit(1))
    if docs:
        _id = docs[0]['_id']
        coll.update({'_id': _id}, {'$set': {'data': args[0], 'commit': True}})
    else:
        doc = {'data': args[0], 'commit': True, 'sid': None, 'tid': None}
        _id = coll.insert(doc)
    return _id


def update(*args):
    _id = ObjectId(args[0])
    data = args[1]
    return coll.update({'_id': _id},
                       {'$set': {'data': data, 'commit': True}})


def delete(*args):
    _id = ObjectId(args[0])
    doc = list(coll.find({'_id': _id}))[0]
    if doc['sid']:
        coll.update({'_id': _id},
                    {'$set': {'data': '', 'commit': True}})
    else:
        coll.remove({'_id': _id})


def up(*args):
    tid = args[0] if len(args) else get_last_tid()
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
    coll.update({'sid': doc['sid']},
                {'$set': {'tid': doc['tid'],
                          'commit': False,
                          'data': doc['data']}},
                safe=True, upsert=True)


def ci():
    url = "%s/%s" % (config.SERVER, get_last_tid())

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
    _id = ObjectId(doc['cid'])
    coll.update({'_id': _id},
                {'$set': {'sid': doc['sid'],
                          'tid': doc['tid'],
                          'commit': False}})

def get_last_tid():
    try:
        docs = coll.find({'tid': {'$gt': 0}})
        docs = docs.sort('tid', -1).limit(1)
        return int(docs.next()['tid'])
    except StopIteration:
        return 0


def get_doc_for_commit(doc):
    _doc = {'cid': str(doc['_id']),
            'data': doc['data']}
    if doc.get('sid'):
        _doc['sid'] = doc['sid']
        _doc['tid'] = doc['tid']
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
