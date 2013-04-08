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

import argparse
import sys
import os
import tempfile
import codecs

try:
    from clint.textui import colored
except:
    colored = None

from lai import config
from lai import Client, Database, Document, Data
from lai import prog, version, description
from lai.database import NotFoundError


COMMANDS = ('search', 'add', 'get', 'edit', 'editor',
            'delete', 'sync', 'copy', 'status',
            '-h', '--help', '-v', '--version')


def _parse_args():

    version_ = '%s %s' % (prog, version)
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('-v', '--version',
                        action='version', version=version_)
    subparsers = parser.add_subparsers(dest='command')

    # Search
    parser_search = subparsers.add_parser('search')
    parser_search.add_argument('regex', help='regular expression to perform the search')
    #parser_search.add_argument('-l', '--limit', help='max of results', default=50)
    #parser_search.add_argument('-c', '--content', action='store_true', help='search into data.content')
    #parser_search.add_argument('-d', '--description', action='store_true', help='search into data.description')
    server_search = parser_search.add_argument_group('server search', 'options for server search')
    server_search.add_argument('-s', '--server', action='store_true', default=False, help='server search in public notes')
    #server_search.add_argument('-u', '--user', nargs='?', help='search in specific user notes')

    # Add
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('content', nargs='?', help='Text for the data.content field')
    parser_add.add_argument('-d', '--description', nargs='?', help='Text for the data.description field')
    parser_add.add_argument('-e', '--editor', action='store_true', help='Use the default editor')
    group_add = parser_add.add_mutually_exclusive_group()
    group_add.add_argument('-p', '--public', action='store_true', dest='public', help='Make the note public')
    group_add.add_argument('-P', '--private', action='store_false', dest='public', help='Make the note private')

    # Get
    parser_get = subparsers.add_parser('get')
    parser_get.add_argument('-v', '--verbose', action='store_true')
    group_get = parser_get.add_mutually_exclusive_group()
    group_get.add_argument('id', nargs='?')
    group_get.add_argument('-a', '--all', action='store_true')

    # Edit
    parser_edit = subparsers.add_parser('edit')
    parser_edit.add_argument('id')
    parser_edit.add_argument('-c', '--content', nargs='?')
    parser_edit.add_argument('-d', '--description', nargs='?')
    parser_edit.add_argument('-e', '--editor', action='store_true', help='Use the default editor')
    group_edit = parser_edit.add_mutually_exclusive_group()
    group_edit.add_argument('-p', '--public', action='store_true', dest='public')
    group_edit.add_argument('-P', '--private', action='store_false', dest='public')

    # Editor
    parser_edit = subparsers.add_parser('editor')
    parser_edit.add_argument('id')

    # Delete
    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('id')

    # Sync
    parser_sync = subparsers.add_parser('sync')
    parser_sync.add_argument('-s', '--server', nargs='?')

    # Copy
    parser_copy = subparsers.add_parser('copy')
    parser_copy.add_argument('id')
    group_copy = parser_copy.add_mutually_exclusive_group()
    group_copy.add_argument('-s', '--from-server', action='store_true')
    group_copy.add_argument('-g', '--to-gist', action='store_true')
    group_copy.add_argument('-c', '--to-clipboard', action='store_true')

    # Status
    parser_status = subparsers.add_parser('status')

    # Search command by default!
    if len(sys.argv) > 1 and sys.argv[1] not in COMMANDS:
        #print "Using search command by default"
        sys.argv[1:1] = ['search']

    args = parser.parse_args()
    return args

def search(args):
    if args.server:
        rs = client.server_search(args.regex)
        _print_search(rs, id_key='sid')
    else:
        rs = client.search(args.regex)
        _print_search(rs, id_key='id')

def _print_search(rs, id_key):
    if rs:
        for doc in rs:
            id = str(getattr(doc, id_key))
            content     = doc.data.content
            description = doc.data.description
            if colored:
                s  = colored.green(id + ': ')
                s += content.encode('utf8')
                if description:
                    s += colored.blue(' #' + description.encode('utf8'))
            else:
                s = "%s: %s" % (id, content.encode('utf8'))
                if description:
                    s += ' #' + description.encode('utf8')
            print s

def add(args):
    if args.content == '-':
        args.content = sys.stdin.read().strip()

    if args.editor:
        args.id = None
        _editor(args)
    else:
        if not args.content:
            sys.exit('Error: content not set')
        doc = Document(Data(args.content, args.description), public=args.public)
        doc = client.save(doc)

def get(args):
    if args.id:
        try:
            doc = client.get(args.id)
        except NotFoundError:
            sys.exit(0)
        if args.verbose:
            for attr in Document.VALID_ATTRS:
                value = getattr(doc, attr)
                if type(value) == list:
                    value = ','.join(value)
                print "%s: %s" % (attr, value)
        else:
            print doc.data.content
    elif args.all:
        docs = client.getall()
        for doc in docs:
            if args.verbose:
                s = "%s: %s" % (doc.id, doc.data.content)
                if doc.data.description:
                    s += ' #' + doc.data.description
            else:
                s = doc.data.content
            print s.encode('utf8')

def edit(args):
    try:
        doc = client.get(args.id)
    except NotFoundError:
        sys.exit('Document not found')
    if args.editor:
        _editor(args)
    else:
        if args.content:
            doc.data.content = args.content
        if args.description:
            doc.data.description = args.description
        doc.public = args.public
        doc = client.save(doc)

def editor(args):
    args.editor = True
    edit(args)

def _get_editor_cmd():
    editor_cmd = os.getenv('EDITOR')
    if editor_cmd is None:
        sys.exit("Environment var EDITOR is unset")
    return editor_cmd

def _editor(args):
    editor_cmd = _get_editor_cmd()

    if args.id:
        try:
            doc = client.get(args.id)
        except NotFoundError:
            sys.exit('Error: Document not found')
    else:
        doc = Document(Data(args.content, args.description), public=args.public)

    (_, filename) = tempfile.mkstemp()

    with codecs.open(filename, 'w', encoding='utf8') as f:
        content_ = getattr(doc.data, 'content') or ''
        description_ = getattr(doc.data, 'description') or ''
        lines = ["### content", content_, "### description", description_]
        data = '\n'.join(lines)
        f.write(data)

    if os.system(editor_cmd + " " + filename) == 0:
        with codecs.open(filename, 'r', encoding='utf8') as f:
            try:
                content, description = _read_data(f)
            except:
                sys.exit('Error: content or description was not found')
            if not content:
                sys.exit('Error: content can not be empty')
            if content_ != content or description_ != description:
                doc.data.content = content
                doc.data.description = description
                client.save(doc)

    os.unlink(filename)

def delete(args):
    try:
        doc = client.get(args.id)
    except NotFoundError:
        sys.exit('Document not found')
    doc = client.delete(doc)

def sync(args):
    conflicts = client.sync()
    if conflicts:
        for inspected in conflicts['docs']:
            if inspected['conflict']:
                inspected['ok_doc'] = _merge_editor(inspected['remote_doc'],
                                                    inspected['local_doc'])
        conflicts = client.sync([i['ok_doc'] for i in conflicts['docs']])

def _merge_editor(remote_doc, local_doc):
    editor_cmd = _get_editor_cmd()
    (_, filename) = tempfile.mkstemp()

    with codecs.open(filename, 'w', encoding='utf8') as f:
        r_content = getattr(remote_doc.data, 'content') or ''
        r_description = getattr(remote_doc.data, 'description') or ''
        l_content = getattr(local_doc.data, 'content') or ''
        l_description = getattr(local_doc.data, 'description') or ''

        lines = [
            "### Conflict detected on doc %s" % remote_doc.sid,
            "### remote content (tid %s)" % remote_doc.tid,
            r_content,
            "### local content (tid %s)" % local_doc.tid,
            l_content,
            "### remote description (tid %s)" % remote_doc.tid,
            r_description,
            "### local description (tid %s)" % local_doc.tid,
            l_description,
            "### Put here the final version",
            "### content",
            "### description",
        ]
        data = '\n'.join(lines)
        f.write(data)

    if os.system(editor_cmd + " " + filename) == 0:
        with codecs.open(filename, 'r', encoding='utf8') as f:
            try:
                content, description = _read_data(f)
            except:
                pass
            else:
                remote_doc.data.content = content
                remote_doc.data.description = description
                remote_doc.merged(True)

    os.unlink(filename)
    return remote_doc

def _read_data(f):
    lines = f.readlines()
    try:
        i_content = lines.index('### content\n')
        i_description = lines.index('### description\n')
    except ValueError:
        raise Exception('Required fields not found')
    content = ''.join(lines[i_content + 1:i_description]).strip()
    description = ''.join(lines[i_description + 1:]).strip()
    return content, description

def copy(args):
    if args.from_server:
        from lai import config
        doc = client.server_get(args.id)
        doc.user = config.USER
        doc.sid  = None
        doc.tid  = None
        client.save(doc)
    else:
        try:
            doc = client.get(args.id)
        except NotFoundError:
            sys.exit('Document not found')
        if args.to_gist:
            html_url = client.send_to_gist(doc)
            print html_url
        elif args.to_clipboard:
            from lai.lib import pyperclip
            if pyperclip.copy is not None:
                pyperclip.copy(doc.data.content)
                print "Copied to clipboard"
            else:
                msg  = 'Can\'t copy the content to the clipboard. '
                msg += 'Do you have xclip installed?'
                sys.exit(msg)

def status(args):
    docs = client.status()
    def print_docs(docs):
        if docs is not None:
            for doc in docs:
                if doc.data is None:
                    data = "[DELETED]"
                else:
                    data = doc.data.content.encode('utf8')
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

if __name__ == '__main__':
    args = _parse_args()
    client = Client(Database(**config.database))
    locals()[args.command](args)
