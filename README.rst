lai
===

Como en el mundo de la informática existen miles de comandos y combinaciones de estos, shortcuts, snippets, trucos, y cosas que querés tener a mano para no olvidarte, lai te permite guardar fácilmente todo esto (y cualquier anotación en gral) en una base de datos local, como sqlite, mysql o mongo, y tenerlos a mano en la consola para cuando los necesites::

    user1@client1:~$ lai --add 'git fetch origin [remote-branch]:[new-local-branch]'

Luego, al buscar por 'git' (lai por default busca)::

    user1@client1:~$ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

También podés traer el documento por su id::

    user1@client1:~$ lai --get 1
    git fetch origin [remote-branch]:[new-local-branch]

Hasta acá nada muy interesante, pero lai trabaja en modo cliente-servidor, por lo que podés tener varios clientes sincronizados contra un servidor central, todo mediante comandos simples como update y commit::

    user1@client1:~$ lai --commit
    Connecting to server..
    Commited! 1 document.

Luego desde otro cliente::

    user1@client2:~$ lai --update
    Connecting to server..
    Updated! 1 document added.
    $ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]


**lai te permite tener todos tus comandos/anotaciones sincronizados entre todas las máquinas que uses.**

lai también soporta usuarios y permite compartir documentos entre ellos::

    user1@client2:~$ lai --adduser 1 user2
    user1@client1:~$ lai --commit
    Connecting to server..
    Commited! 1 document.

Luego el usuario user2 descarga el documento compartido::

    user2@client1:~$ lai --update
    Connecting to server..
    Updated! 1 document added.
    $ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

