# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import codecs
import pyperclip

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
        sys.stdout.write('Argument TEXT required\n')
        return None
    doc = Document(data)
    if len(args) == 2:
        doc.set_keys(args[1])
    try:
        doc = client.save(doc)
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')

def get(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stdout.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')
    if doc.data:
        print doc.data

def getall(*args):
    docs = client.getall()
    for doc in docs:
        print "%d: %s" % (doc.id, doc.data)

def clip(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stdout.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')
    if doc.data:
        pyperclip.copy(doc.data)
        print doc.data

def show(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stdout.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')
    if doc:
        for key in ('id', 'sid', 'tid', 'synched',
                    'users', 'usersdel', 'keys', 'data'):
            value = getattr(doc, key)
            if type(value) == list:
                value = ','.join(value)
            print "%s: %s" % (key, value)

def edit(*args):
    try:
        id = args[0]
        data = args[1]
    except IndexError:
        sys.stdout.write('Arguments ID and NEW_TEXT required\n')
        return None
    doc = client.get(id)
    doc.data = data
    try:
        doc = client.save(doc)
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')

def delete(*args):
    try:
        doc = client.get(args[0])
    except IndexError:
        sys.stdout.write('Argument ID required\n')
    try:
        doc = client.delete(doc)
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')

def search(q):
    try:
        rs = client.search(q)
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')
    if rs:
        for doc in rs:
            if colored:
                tokens = doc.data.rsplit('#')
                s  = colored.blue(str(doc.id) + ': ')
                s += tokens[0].strip().encode('utf8')
                if len(tokens) == 2:
                    s += colored.green(' #' + tokens[1].encode('utf8'))
                print s
            else:
                print "%s: %s" % (doc.id, doc.data.encode('utf8'))

def update(*args):
    try:
        rs = client.update()
        if rs is None:
            print "Nothing to update"
        else:
            print "Updated %d documents" % rs
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')

def commit(*args):
    try:
        rs = client.commit()
        if rs is None:
            print "Nothing to commit"
        else:
            print "Commited %d documents" % rs
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')

def editor(*args):
    editor_cmd = os.getenv('EDITOR')
    keys_line = '------------- enter keywords before this line -------------'

    if editor_cmd is None:
        sys.stdout.write("Environment var EDITOR is unset\n")
        return None

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
    try:
        docs = client.status()
    except ClientException as e:
        sys.stdout.write(str(e) + '\n')
    for doc in docs:
        if doc.data is None:
            data = "[DELETED]"
        else:
            data = doc.data
        print "%d: %s" % (doc.id, data[:70])

def adduser(*args):
    try:
        return _set_user('add', *args)
    except (IndexError, TypeError):
        sys.stdout.write('Arguments ID and USER required\n')

def deluser(*args):
    try:
        return _set_user('del', *args)
    except (IndexError, TypeError):
        sys.stdout.write('Arguments ID and USER required\n')

def send_to_gist(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stdout.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
        html_url = client.send_to_gist(doc)
        sys.stdout.write(html_url + '\n')

    except ClientException as e:
        sys.stdout.write(str(e) + '\n')

def _set_user(action, id, user):
    doc = client.get(id)
    if action == 'add':
        rs = doc.add_user(user)
    elif action == 'del':
        rs = doc.del_user(user)
    if rs == True:
        try:
            doc = client.save(doc)
        except ClientException as e:
            sys.stdout.write(str(e) + '\n')
    else:
        sys.stdout.write('Can\'t %s user\n' % action)

def print_short_help():
    out  = "Usage: lai WORD\n"
    out += "       lai [--update | --commit | --status]\n"
    out += "       lai [--add TEXT | --edit ID NEW_TEXT | --editor [ID]]\n"
    out += "       lai [--get ID | --clip ID | --show ID | --del ID | --getall]\n"
    out += "       lai [--adduser ID USER | --deluser ID USER]\n"
    out += "       lai [--gist ID]\n"
    out += "       lai [--help]"
    print out

def print_long_help():
    out  = "Usage: lai WORD                  Performs a search\n"
    out += "       lai --add TEXT            Add new doc\n"
    out += "       lai --edit ID NEW_TEXT    Edit doc\n"
    out += "       lai --editor [ID]         Add or edit with default text editor\n"
    out += "       lai --get ID              Get a specific doc\n"
    out += "       lai --clip ID             Show and copy to clipboard a specific doc\n"
    out += "       lai --getall              Get all docs\n"
    out += "       lai --show ID             Show all metadata from a specific doc\n"
    out += "       lai --del ID              Delete doc\n"
    out += "       lai --gist ID             Send doc to Github Gist\n"
    out += "       lai --update              Update changes from server\n"
    out += "       lai --commit              Commit changes to server\n"
    out += "       lai --status              Show actual status\n"
    out += "       lai --adduser ID USER     Add user to doc\n"
    out += "       lai --deluser ID USER     Del user from doc"
    print out


if __name__ == '__main__':
    try:
        client = Client(Database())
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')
    else:
        METHODS = {
            '--get'    : get,
            '--getall' : getall,
            '--clip'   : clip,
            '--show'   : show,
            '--add'    : add,
            '--edit'   : edit,
            '--del'    : delete,
            '--commit' : commit,
            '--update' : update,
            '--editor' : editor,
            '--status' : status,
            '--adduser': adduser,
            '--deluser': deluser,
            '--gist'   : send_to_gist,
            '--help'   : print_long_help,
        }

        if len(sys.argv) > 1:
            rs = None
            if sys.argv[1].startswith('--'):
                try:
                    fn = METHODS[sys.argv[1]]
                except KeyError:
                    sys.stderr.write('Invalid argument\n')
                else:
                    if len(sys.argv) > 2:
                        rs = fn(*sys.argv[2:])
                    else:
                        rs = fn()
            else:
                search(sys.argv[1])
        else:
            print_short_help()

