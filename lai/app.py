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
# GNU General Public License for more details.
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

from lai import Client, Database, Document, Data
from lai.database import NotFoundError


def add(*args):
    try:
        content = args[0].strip()
    except IndexError:
        sys.exit('Argument TEXT required')
    try:
        help = args[1]
    except IndexError:
        help = None
    doc = Document(Data(content, help))
    doc = client.save(doc)

def get(*args):
    try:
        id = args[0]
    except IndexError:
        sys.exit('Argument ID required')
    try:
        doc = client.get(id)
    except NotFoundError:
        pass
    else:
        print doc.data.content

def getall(*args):
    docs = client.getall()
    for doc in docs:
        s = "%s: %s" % (doc.id, doc.data.content)
        if doc.data.help:
            s += ' :' + doc.data.help
        print s.encode('utf8')

def clip(*args):
    try:
        id = args[0]
    except IndexError:
        sys.exit('Argument ID required')
    doc = client.get(id)
    if doc.data:
        import pyperclip
        if pyperclip.copy is not None:
            pyperclip.copy(doc.data)
            print doc.data
        else:
            sys.exit('Can\'t copy the content to the clipboard. Do you have xclip installed?')

def show(*args):
    try:
        id = args[0]
    except IndexError:
        sys.exit('Argument ID required')
    try:
        doc = client.get(id)
    except NotFoundError:
        pass
    else:
        for attr in Document.VALID_ATTRS:
            value = getattr(doc, attr)
            if type(value) == list:
                value = ','.join(value)
            print "%s: %s" % (attr, value)

def edit(*args):
    try:
        id = args[0]
        content = args[1].strip()
    except IndexError:
        sys.exit('Arguments ID and TEXT required')
    try:
        doc = client.get(id)
    except NotFoundError:
        sys.exit('Document not found')
    save = False
    if content != '':
        doc.data.content = content
        save = True
    if len(args) == 3:
        doc.data.help = args[2].strip()
        save = True
    if save:
        doc = client.save(doc)

def delete(*args):
    try:
        doc = client.get(args[0])
    except IndexError:
        sys.exit('Argument ID required')
    doc = client.delete(doc)

def search(regex):
    rs = client.search(regex)
    _print_search(rs, id_key='id')

def server_search(*args):
    try:
        regex = args[0]
    except IndexError:
        sys.exit('Argument REGEX required')
    rs = client.server_search(regex)
    _print_search(rs, id_key='sid')

def _print_search(rs, id_key):
    if rs:
        for doc in rs:
            id      = str(getattr(doc, id_key))
            content = doc.data.content
            help    = doc.data.help
            if colored:
                s  = colored.green(id + ': ')
                s += content.encode('utf8')
                if help:
                    s += colored.blue(' :' + help.encode('utf8'))
            else:
                s = "%s: %s" % (id, content.encode('utf8'))
                if help:
                    s += ' :' + help.encode('utf8')
            print s

def copy(*args):
    try:
        sid = args[0]
    except IndexError:
        sys.exit('Argument SID required')
    from lai import config
    doc = client.server_get(sid)
    doc.user = config.USER
    doc.sid  = None
    doc.tid  = None
    client.save(doc)

def sync(*args):
    client.sync()

def editor(*args):
    editor_cmd = os.getenv('EDITOR')

    if editor_cmd is None:
        sys.exit("Environment var EDITOR is unset")

    if len(args):
        doc = client.get(args[0])
    else:
        doc = Document()

    (_, filename) = tempfile.mkstemp()

    with codecs.open(filename, 'w', encoding='utf8') as file:
        data = "" if doc.data is None else doc.data.content
        file.write(data)

    if os.system(editor_cmd + " " + filename) == 0:
        with codecs.open(filename, 'r', encoding='utf8') as file:
            doc.data = file.read().strip()
            if doc.data or doc.id:
                client.save(doc)

    os.unlink(filename)

def set_public(*args):
    _set('public', True, *args)

def unset_public(*args):
    _set('public', False, *args)

def _set(key, value, *args):
    try:
        id = args[0]
    except IndexError:
        sys.exit('Argument ID required')
    doc = client.get(id)
    setattr(doc, key, value)
    client.save(doc)

def status(*args):
    docs = client.status()
    def print_docs(docs):
        if docs is not None:
            for doc in docs:
                if doc.data is None:
                    data = "[DELETED]"
                else:
                    data = doc.data.content
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
        sys.exit('Argument ID required')
    doc = client.get(id)
    html_url = client.send_to_gist(doc)
    sys.stderr.write(html_url + '\n')

def print_short_help():
    out  = "Usage: lai REGEX\n"
    out += "       lai [--sync | --status]\n"
    out += "       lai [--add TEXT [HELP] | --edit ID TEXT [HELP] | --editor [ID]]\n"
    out += "       lai [--get ID | --clip ID | --show ID | --del ID | --getall]\n"
    out += "       lai [--set-public ID | --unset-public ID]\n"
    out += "       lai [--server-search REGEX | --copy SID]\n"
    out += "       lai [--gist ID]\n"
    out += "       lai [--help | --version]"
    print out

def print_long_help():
    out  = "Usage: lai REGEX                  Performs a regex search\n"
    out += "       lai --add TEXT [HELP]      Add new doc\n"
    out += "       lai --edit ID TEXT [HELP]  Edit inline a doc\n"
    out += "       lai --editor [ID]          Add or edit with default text editor\n"
    out += "       lai --get ID               Get a specific doc\n"
    out += "       lai --clip ID              Show and copy to clipboard a specific doc\n"
    out += "       lai --getall               Get all docs\n"
    out += "       lai --del ID               Delete doc\n"
    out += "       lai --gist ID              Send doc to Github Gist\n"
    out += "       lai --set-public ID        Set public a doc\n"
    out += "       lai --unset-public ID      Unset public a doc\n"
    out += "       lai --server-search REGEX  Performs a regex search in server\n"
    out += "       lai --copy SID             Copy a public doc from server\n"
    out += "       lai --show ID              Show all metadata from a specific doc\n"
    out += "       lai --status               Show docs to sync\n"
    out += "       lai --sync                 Sync changes with server\n"
    out += "       lai --help                 Show this help\n"
    out += "       lai --version              Show program version"
    print out

def print_version():
    from lai import version
    print "lai-client", version


if __name__ == '__main__':
    client = Client(Database())

    METHODS = {
        '--get'          : get,
        '--getall'       : getall,
        '--clip'         : clip,
        '--show'         : show,
        '--add'          : add,
        '--edit'         : edit,
        '--del'          : delete,
        '--sync'         : sync,
        '--editor'       : editor,
        '--set-public'   : set_public,
        '--unset-public' : unset_public,
        '--server-search': server_search,
        '--copy'         : copy,
        '--status'       : status,
        '--gist'         : send_to_gist,
        '--help'         : print_long_help,
        '--version'      : print_version,
    }

    if len(sys.argv) > 1:
        rs = None
        if sys.argv[1].startswith('--'):
            try:
                fn = METHODS[sys.argv[1]]
            except KeyError:
                sys.exit('Invalid argument')
            else:
                if len(sys.argv) > 2:
                    rs = fn(*sys.argv[2:])
                else:
                    rs = fn()
        else:
            search(sys.argv[1])
    else:
        print_short_help()

