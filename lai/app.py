# -*- coding: utf-8 -*-

# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import tempfile
import codecs

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
        sys.stderr.write('Argument TEXT required\n')
        return None
    doc = Document(data)
    try:
        doc = client.save(doc)
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')

def get(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stderr.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')
    if doc.data:
        print doc.data['body']

def getall(*args):
    docs = client.getall()
    for doc in docs:
        print "%d: %s" % (doc.id, doc.data['body'])

def clip(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stderr.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')
    if doc.data:
        import pyperclip
        if pyperclip.copy is not None:
            pyperclip.copy(doc.data)
            print doc.data
        else:
            sys.stderr.write('Can\'t copy the content to the clipboard. Do you have xclip installed?\n')

def show(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stderr.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')
    if doc:
        for key in ('id', 'sid', 'tid', 'public', 'synced', 'data'):
            value = getattr(doc, key)
            if type(value) == list:
                value = ','.join(value)
            print "%s: %s" % (key, value)

def edit(*args):
    try:
        id = args[0]
        data = args[1]
    except IndexError:
        sys.stderr.write('Arguments ID and NEW_TEXT required\n')
        return None
    doc = client.get(id)
    doc.data = data
    try:
        doc = client.save(doc)
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')

def delete(*args):
    try:
        doc = client.get(args[0])
    except IndexError:
        sys.stderr.write('Argument ID required\n')
    try:
        doc = client.delete(doc)
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')

def search(q):
    try:
        rs = client.search(q)
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')
    if rs:
        for doc in rs:
            if colored:
                tokens = doc.data['body'].rsplit('#')
                s  = colored.blue(str(doc.id) + ': ')
                s += tokens[0].strip().encode('utf8')
                if len(tokens) == 2:
                    s += colored.green(' #' + tokens[1].encode('utf8'))
                print s
            else:
                print "%s: %s" % (doc.id, doc.data['body'].encode('utf8'))

def sync(*args):
    try:
        client.sync()
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')

def editor(*args):
    editor_cmd = os.getenv('EDITOR')

    if editor_cmd is None:
        sys.stderr.write("Environment var EDITOR is unset\n")
        return None

    if len(args):
        doc = client.get(args[0])
    else:
        doc = Document()

    (_, filename) = tempfile.mkstemp()

    with codecs.open(filename, 'w', encoding='utf8') as file:
        data = "" if doc.data is None else doc.data['body']
        file.write(data)

    if os.system(editor_cmd + " " + filename) == 0:
        with codecs.open(filename, 'r', encoding='utf8') as file:
            doc.data = file.read().strip()
            if doc.data or doc.id:
                client.save(doc)

    os.unlink(filename)

def status(*args):
    try:
        docs = client.status()
    except ClientException as e:
        sys.stderr.write(str(e) + '\n')
    def print_docs(docs):
        if len(docs):
            for doc in docs:
                if doc.data is None:
                    data = "[DELETED]"
                else:
                    data = doc.data['body']
                print "{:>6}: {:.70}".format(doc.id, data)
        else:
            print "None"
    fmt = "{:-^80}"
    print fmt.format('Updated')
    print_docs(docs['updated'])
    print fmt.format('Committed')
    print_docs(docs['committed'])
    print fmt.format('To commit')
    print_docs(docs['to_commit'])

def send_to_gist(*args):
    try:
        id = args[0]
    except IndexError:
        sys.stderr.write('Argument ID required\n')
        return None
    try:
        doc = client.get(id)
        html_url = client.send_to_gist(doc)
        sys.stderr.write(html_url + '\n')

    except ClientException as e:
        sys.stderr.write(str(e) + '\n')

def print_short_help():
    out  = "Usage: lai REGEX\n"
    out += "       lai [--sync | --status]\n"
    out += "       lai [--add TEXT | --edit ID NEW_TEXT | --editor [ID]]\n"
    out += "       lai [--get ID | --clip ID | --show ID | --del ID | --getall]\n"
    out += "       lai [--gist ID]\n"
    out += "       lai [--help | --version]"
    print out

def print_long_help():
    out  = "Usage: lai REGEX                 Performs a regex search\n"
    out += "       lai --add TEXT            Add new doc\n"
    out += "       lai --edit ID NEW_TEXT    Edit inline a doc\n"
    out += "       lai --editor [ID]         Add or edit with default text editor\n"
    out += "       lai --get ID              Get a specific doc\n"
    out += "       lai --clip ID             Show and copy to clipboard a specific doc\n"
    out += "       lai --getall              Get all docs\n"
    out += "       lai --show ID             Show all metadata from a specific doc\n"
    out += "       lai --del ID              Delete doc\n"
    out += "       lai --gist ID             Send doc to Github Gist\n"
    out += "       lai --sync                Sync changes with server\n"
    out += "       lai --status              Show docs to sync\n"
    out += "       lai --help                Show this help\n"
    out += "       lai --version             Show program version"
    print out

def print_version():
    from lai import version
    print "lai-client", version


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
            '--sync'   : sync,
            '--editor' : editor,
            '--status' : status,
            '--gist'   : send_to_gist,
            '--help'   : print_long_help,
            '--version': print_version,
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

