# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import codecs

from lai import Client, Database, Document


client = Client(Database())


def save(*args):
    doc = Document(args[0])
    client.save(doc)


def editor(*args):
    if len(args):
        doc = client.get(args[0])
    else:
        doc = Document()

    (_, filename) = tempfile.mkstemp()

    if doc.id:
        file = codecs.open(filename, 'w', encoding='utf8')
        file.write(doc.data)
        file.close()

    if os.system(os.getenv('EDITOR') + " " + filename) == 0:
        doc.data = codecs.open(filename, 'r', encoding='utf8').read()
        client.save(doc)

    os.unlink(filename)


def print_result(rs):
    if type(rs) == list:
        fmt = "%-24s | %-24s | %-5s | %-5s | %s"
        print fmt % ('id', 'sid', 'tid', 'data', 'keys')
        for doc in rs:
            print fmt % (doc.id, doc.sid, doc.tid,
                         doc.data, doc.keys)
    elif type(rs) == dict:
        pprint(rs)
    elif rs is not None:
        print rs


def print_help(msg=None):
    if msg:
        print msg
        print
    print "Usage: lai regex                 Performs a regex search"
    print "       lai --add 'Text.'         Add new doc"
    print "       lai --get [ID]            Get all or a specific doc"
    print "       lai --edit ID 'New text'  Update doc"
    print "       lai --editor [ID]         Add or Update doc with default text editor"
    print "       lai --delete ID           Delete doc"
    print "       lai --update              Update changes"
    print "       lai --commit              Commit changes"



METHODS = {
    '--get'    : client.get,
    '--add'    : save,
    #'--edit'   : edit,
    #'--delete' : delete,
    '--commit' : client.commit,
    '--update' : client.update,
    '--editor' : editor,
    '--help'   : print_help,
}


if len(sys.argv) > 1:
    rs = None
    if sys.argv[1].startswith('--'):
        try:
            fn = METHODS[sys.argv[1]]
        except KeyError:
            print_help("Method not implemented.")
        else:
            if len(sys.argv) > 2:
                rs = fn(*sys.argv[2:])
            else:
                rs = fn()
    else:
        rs = client.search(sys.argv[1])
    print_result(rs)
else:
    print_help()

