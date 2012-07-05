# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import codecs
from pprint import pprint

try:
    from clint.textui import colored
except:
    colored = None

from lai import Client, Database, Document
from lai.client import ClientException


def add(*args):
    try:
        data = args[0]
    except IndexError:
        return get_short_help("Argument TEXT required")
    else:
        doc = Document(data)
        if len(args) == 2:
            doc.set_keys(args[1])
        try:
            client.save(doc)
        except ClientException as e:
            return e

def get(*args):
    try:
        id = args[0]
    except IndexError:
        return get_short_help("Argument ID required")
    else:
        doc = client.get(id)
        if doc:
            return [doc]

def edit(*args):
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
    keys_line = '------------- enter keywords before this line -------------'

    if editor_cmd is None:
        return to_stdout("Environment var EDITOR is unset")

    if len(args):
        doc = client.get(args[0])
    else:
        doc = Document()

    (_, filename) = tempfile.mkstemp()

    with codecs.open(filename, 'w', encoding='utf8') as file:
        data = doc.data or ''
        keys = doc.keys or ''
        file.write("%s\n%s\n%s" % (data, keys_line, keys))

    rs = None
    if os.system(editor_cmd + " " + filename) == 0:
        with codecs.open(filename, 'r', encoding='utf8') as file:
            lines = file.read().splitlines()
            end_data = None
            if keys_line in lines:
                end_data = lines.index(keys_line)
                if len(lines) > end_data + 1:
                    doc.set_keys('\n'.join(lines[end_data + 1:]))
            if end_data is not None:
                lines = lines[:end_data]
            doc.data = '\n'.join(lines).strip()
            if doc.data:
                rs = client.save(doc)

    os.unlink(filename)
    return rs

def status(*args):
    rs = client.status()
    if rs:
        return rs
    return None

def adduser(*args):
    try:
        return _set_user('add', *args)
    except (IndexError, TypeError):
        return get_short_help("Arguments ID and USER required")

def deluser(*args):
    try:
        return _set_user('del', *args)
    except (IndexError, TypeError):
        return get_short_help("Arguments ID and USER required")

def _set_user(action, id, user):
    doc = client.get(id)
    if action == 'add':
        rs = doc.add_user(user)
    elif action == 'del':
        rs = doc.del_user(user)
    if rs == True:
        return client.save(doc)
    return False

def to_stdout(obj, verbose=False):
    if type(obj) == list:
        if verbose:
            fmt = "%-4s | %-24s | %-4s | %-7s | %-14s | %s\n%s"
            print fmt % ('id', 'sid', 'tid', 'synched', 'users', 'keys', '-'*80)
            for doc in obj:
                print fmt % (doc.id, doc.sid, doc.tid, doc.synched,
                             ','.join(doc.users), doc.keys,
                             "%s\n%s" % (doc.data, '-'*80))
        else:
            for doc in obj:
                if colored:
                    tokens = doc.data.rsplit('#')
                    s  = colored.blue(str(doc.id) + ': ')
                    s += tokens[0].strip().encode('utf8')
                    if len(tokens) == 2:
                        s += colored.green(' #' + tokens[1].encode('utf8'))
                    print s
                else:
                    print "%s: %s" % (doc.id, doc.data.encode('utf8'))
    elif type(obj) == dict:
        pprint(obj)
    elif obj is not None:
        print obj

def get_short_help(msg=None):
    out = ''
    if msg:
        out = msg + '\n\n'
    out += "Usage: lai WORD\n"
    out += "       lai [--update | --commit | --status]\n"
    out += "       lai [--add TEXT | --edit ID NEW_TEXT | --editor [ID]]\n"
    out += "       lai [--get ID | --del ID]\n"
    out += "       lai [--adduser ID USER | --deluser ID USER]"
    return out

def get_long_help(msg=None):
    out = ''
    if msg:
        out = msg + '\n\n'
    out += "Usage: lai WORD                  Performs a search\n"
    out += "       lai --add TEXT            Add new doc\n"
    out += "       lai --edit ID NEW_TEXT    Edit doc\n"
    out += "       lai --editor [ID]         Add or edit with default text editor\n"
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
    
    try:
        client = Client(Database())
    except ClientException as e:
        sys.stderr.write("%s\n" % e)
    else:
        METHODS = {
            '--get'    : get,
            '--add'    : add,
            '--edit'   : edit,
            '--del'    : delete,
            '--commit' : commit,
            '--update' : update,
            '--editor' : editor,
            '--status' : status,
            '--adduser': adduser,
            '--deluser': deluser,
            '--help'   : lambda: to_stdout(get_long_help()),
        }

        verbose = True
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
                verbose = False
            to_stdout(rs, verbose=verbose)
        else:
            to_stdout(get_long_help())

