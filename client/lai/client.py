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


def search(regex):
    return list(coll.find({'data': {'$regex': regex}}))


def get(*args):
    params = {'_id': ObjectId(args[0])} if len(args) else {}
    return list(coll.find(params))


def add(*args):
    # Search for a doc without data
    docs = list(coll.find({'data': ''}).limit(1))
    if len(docs) == 1:
        _id = docs[0]['_id']
        coll.update({'_id': _id}, {'$set': {'data': args[0], 'commit': True}})
    else:
        doc = {'data': args[0], 'commit': True, 'sid': None, 'tid': None}
        _id = coll.insert(doc)
    return _id


def put(*args):
    _id = ObjectId(args[0])
    data = args[1]
    rs = coll.update({'_id': _id},
                     {'$set': {'data': data, 'commit': True}},
                     safe=True)
    return rs['n'] == 1


def delete(*args):
    _id = ObjectId(args[0])
    doc = list(coll.find({'_id': _id}))[0]
    if doc['sid']:
        rs = coll.update({'_id': _id},
                         {'$set': {'data': '', 'commit': True}},
                         safe=True)
    else:
        rs = coll.remove({'_id': _id}, safe=True)
    return rs['n'] == 1


def update(*args):
    tid = args[0] if len(args) else get_last_tid()
    url = "%s/%s" % (config.SERVER, tid)
    req = urllib2.urlopen(url)
    data = json.loads(req.read())
    if len(data['docs']):
        for doc in data['docs']:
            rs = process_update(doc)
            print "%s %s" % (doc['sid'], rs['n'] == 1)
        return "%d docs updated" % len(data['docs'])
    else:
        return "nothing to update"


def process_update(doc):
    return coll.update({'sid': doc['sid']},
                       {'$set': {'tid': doc['tid'],
                                 'commit': False,
                                 'data': doc['data']}},
                       safe=True, upsert=True)


def commit():
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
                rs = process_commit(doc)
                print "%s %s" % (doc['cid'], rs['n'] == 1)
            return "%d docs commited" % len(data['docs'])
    else:
        return "nothing to commit"


def process_commit(doc):
    _id = ObjectId(doc['cid'])
    return coll.update({'_id': _id},
                       {'$set': {'sid': doc['sid'],
                                 'tid': doc['tid'],
                                 'commit': False}},
                       safe=True)


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


def print_result(rs):
    if type(rs) == list:
        fmt = "%-24s | %-24s | %-5s | %-5s | %s"
        print fmt % ('_id', 'sid', 'tid', 'ci', 'data')
        for doc in rs:
            print fmt % (doc['_id'], doc['sid'], doc['tid'],
                         doc['commit'], doc['data'])
    elif type(rs) == dict:
        pprint(rs)
    elif rs is not None:
        print rs


def print_help(msg=None):
    if msg:
        print msg
        print
    print "Usage: lai regex                 Performs a regex search"
    print "       lai --add 'Text.'         Add new document"
    print "       lai --get [ID]            Get all or specific document"
    print "       lai --put ID 'New text'   Update document"
    print "       lai --del ID              Delete document"
    print "       lai --update              Update changes"
    print "       lai --commit              Commit changes"


METHODS = {
    'get'    : get,
    'add'    : add,
    'put'    : put,
    'del'    : delete,
    'delete' : delete,
    'commit' : commit,
    'ci'     : commit,
    'update' : update,
    'up'     : update,
    'help'   : print_help,
}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        rs = None
        if sys.argv[1].startswith('--'):
            try:
                fn = METHODS[sys.argv[1][2:]]
            except KeyError:
                print_help("Method not implemented.")
            else:
                if len(sys.argv) > 2:
                    rs = fn(*sys.argv[2:])
                else:
                    rs = fn()
        else:
            rs = search(sys.argv[1])
        print_result(rs)
    else:
        print_help()

