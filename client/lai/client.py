# -*- coding: utf-8 -*-

## tid = transaction_id

import sys
import urllib2
import json
import pymongo


SERVER_HOST = 'http://localhost:8888/'

conn = pymongo.Connection()
db = conn.lai_client


def get(*args):
    id = int(args[0]) if len(args) else 0
    params = {'_id': id} if id else {}
    for doc in db.docs.find(params):
        print doc

def add(*args):
    doc = {'data': args[0],
           'commit': True}
    db.docs.insert(doc)

def up(*args):
    tid = args[0] if len(args) else 0
    url = SERVER_HOST + str(tid)
    print "request", url
    req = urllib2.urlopen(url)
    docs = json.loads(req.read())
    for doc in docs:
        print doc

#def maxtid():
#   r = db.docs.find().sort({'tid': -1}).limit(1)
#   if r:
#       return r['tid']
#   else:
#       return 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            if len(sys.argv) > 2:
                globals()[sys.argv[1]](*sys.argv[2:])
            else:
                globals()[sys.argv[1]]()
        except KeyError:
            print "Method not implemented"
    else:
        print "Usage: lai METHOD [arg1 [, argn]]"
