# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import codecs
from pprint import pprint

from lai import Client, Database, Document


def add(*args):
    try:
        data = args[0]
    except IndexError:
        return get_short_help("Argument TEXT required")
    else:
        doc = Document(data)
        return client.save(doc)

def get(*args):
    try:
        id = args[0]
    except IndexError:
        return get_short_help("Argument ID required")
    else:
        doc = client.get(id)
        if doc:
            return [doc]

def change(*args):
    try:
        id = args[0]
        data = args[1]
    except IndexError:
        return get_short_help("Arguments ID and NEW_TEXT required")
    else:
        doc = client.get(id)
        doc.data = data
        return client.save(doc)

def delete(*args):
    try:
        doc = client.get(args[0])
    except IndexError:
        return get_short_help("Argument ID required")
    else:
        return client.delete(doc)

def search(q):
    rs = client.search(q)
    if rs:
        return rs
    return None

def update(*args):
    return client.update()

def commit(*args):
    return client.commit()

def editor(*args):
    editor_cmd = os.getenv('EDITOR')

    if editor_cmd is None:
        return to_stdout("Environment var EDITOR is unset")

    if len(args):
        doc = client.get(args[0])
    else:
        doc = Document()

    (_, filename) = tempfile.mkstemp()

    if doc.id:
        file = codecs.open(filename, 'w', encoding='utf8')
        file.write(doc.data)
        file.close()

    rs = None
    if os.system(editor_cmd + " " + filename) == 0:
        doc.data = codecs.open(filename, 'r', encoding='utf8').read()
        rs = client.save(doc)

    os.unlink(filename)
    return rs

def status(*args):
    return "Not implemented yet"

def adduser(*args):
    return _change_user('add', args)

def deluser(*args):
    return _change_user('del', args)

def _change_user(type, args):
    try:
        id = args[0]
        user = args[1]
    except IndexError:
        return get_short_help("Arguments ID and USER required")
    else:
        doc = client.get(id)
        if type == 'add':
            doc.add_user(user)
        elif type == 'del':
            doc.del_user(user)
        client.save(doc)

def to_stdout(obj):
    if type(obj) == list:
        fmt = "%-4s | %-24s | %-4s | %-14s | %s\n%s"
        print fmt % ('id', 'sid', 'tid', 'users', 'keys', '-'*80)
        for doc in obj:
            print fmt % (doc.id, doc.sid, doc.tid,
                         ','.join(doc.users), doc.keys,
                         "%s\n%s" % (doc.data, '-'*80))
    elif type(obj) == dict:
        pprint(obj)
    elif obj is not None:
        print obj

def get_short_help(msg=None):
    out = ''
    if msg:
        out = msg + '\n\n'
    out += "Usage: lai regex\n"
    out += "       lai [--update | --commit | --status]\n"
    out += "       lai [--add TEXT | --change ID NEW_TEXT | --editor [ID]]\n"
    out += "       lai [--get ID | --del ID]\n"
    out += "       lai [--adduser ID USER | --deluser ID USER]"
    return out

def get_long_help(msg=None):
    out = ''
    if msg:
        out = msg + '\n\n'
    out += "Usage: lai regex                 Performs a regex search\n"
    out += "       lai --add TEXT            Add new doc\n"
    out += "       lai --change ID NEW_TEXT  Update doc\n"
    out += "       lai --editor [ID]         Add or Update doc with default text editor\n"
    out += "       lai --get ID              Get a specific doc\n"
    out += "       lai --del ID              Delete doc\n"
    out += "       lai --update              Update changes\n"
    out += "       lai --commit              Commit changes\n"
    out += "       lai --status              Show actual status\n"
    out += "       lai --adduser ID USER     Add user to doc\n"
    out += "       lai --deluser ID USER     Del user from doc"
    return out

    out = ""
    if msg:
        out = msg + '\n'


if __name__ == '__main__':

    client = Client(Database())

    METHODS = {
        '--get'    : get,
        '--add'    : add,
        '--change' : change,
        '--del'    : delete,
        '--commit' : commit,
        '--update' : update,
        '--editor' : editor,
        '--status' : status,
        '--adduser': adduser,
        '--deluser': deluser,
        '--help'   : lambda: to_stdout(get_long_help()),
    }

    if len(sys.argv) > 1:
        rs = None
        if sys.argv[1].startswith('--'):
            try:
                fn = METHODS[sys.argv[1]]
            except KeyError:
                to_stdout(get_long_help("Invalid argument"))
            else:
                if len(sys.argv) > 2:
                    rs = fn(*sys.argv[2:])
                else:
                    rs = fn()
        else:
            rs = search(sys.argv[1])
        to_stdout(rs)
    else:
        to_stdout(get_long_help())

