lai
===

Es un sencillo programa de línea de comandos que permite guardar anotaciones y mantenerlas sincronizadas entre varias computadoras. La idea es guardarte comandos, shortcuts, snippets y en gral cualquier cosa que quieras tener a mano en la consola. También podés compartir documentos con otros usuarios::

    juan@compu1:~$ lai --add 'git fetch origin [remote-branch]:[new-local-branch]'

Luego, al buscar por 'git' (por defecto lai busca)::

    juan@compu1:~$ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

También podés traer el documento por su id::

    juan@compu1:~$ lai --get 1
    git fetch origin [remote-branch]:[new-local-branch]

Como lai trabaja en modo cliente-servidor podés tener varios clientes sincronizados contra un servidor central, todo mediante comandos simples como update y commit::

    juan@compu1:~$ lai --commit
    Connecting to server..
    Commited! 1 document.

Luego desde otro cliente::

    juan@client2:~$ lai --update
    Connecting to server..
    Updated! 1 document added.
    $ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

lai también soporta usuarios y permite compartir documentos entre ellos::

    juan@client2:~$ lai --adduser 1 paula
    juan@compu1:~$ lai --commit
    Connecting to server..
    Commited! 1 document.

Luego el usuario paula descarga el documento compartido::

    paula@compu1:~$ lai --update
    Connecting to server..
    Updated! 1 document added.
    $ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

