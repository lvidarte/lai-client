import sys
import urllib2
import json
import pymongo

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
    oid = args[0] if len(args) else 0
    url = 'http://localhost:8888/%s' % oid
    req = urllib2.urlopen(url)
    docs = json.loads(req.read())
    for doc in docs:
        print doc

def maxoid():
    r = db.docs.find().sort({'oid': -1}).limit(1)
    if r:
        return r['oid']
    else:
        return 0


if __name__ == '__main__':
    try:
        if len(sys.argv) > 2:
            globals()[sys.argv[1]](*sys.argv[2:])
        else:
            globals()[sys.argv[1]]()
    except KeyError:
        print "Method not implemented"
