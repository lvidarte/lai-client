lai
===

lai is a command line program to store notes and keep them synchronized between multiple computers. The idea is to keep your commands, shortcuts, snippets and anything you want to have on hand at the console. You can also share notes with others::

Store a note::

    $ lai add 'grep -R <pattern> --include \*.txt <dir>'

Search::

    $ lai search grep
    1: grep -R <pattern> --include \*.txt <dir>

Share with others::

    $ lai edit 1 --public

Sync with server::

    $ lai sync

Search in public notes::

    $ lai search --server grep
    5015d7273042976dc5000230: egrep -w 'word1|word2' /path/to/file
    5015d7363042976dc500031b: grep -i ps ~/.bash* | grep -v history

Copy from server::

    $ lai copy --server 5015d7273042976dc5000230

