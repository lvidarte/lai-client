Lai:

lai te permite guardar fácilmente comandos, snippets, y anotaciones en gral, en una base de datos local (mongo, sqlite, mysql, etc..) y tenerlas a mano en la consola para cuando las necesites:

    cliente-1~$ lai --add 'git fetch origin [remote-branch]:[new-local-branch]'

Luego, al buscar por 'git'

    xleo@client1:~$ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

También podemos traer el documento por su id:

    xleo@client1:~$ lai --get 1
    git fetch origin [remote-branch]:[new-local-branch]

Hasta acá nada muy interesante, pero lai trabaja en modo cliente-servidor, por lo que podés tener varios clientes sincronizados contra un servidor central, todo mediante comandos simples como update y commit.

    xleo@client1:~$ lai --commit
    Connecting to server..
    Commited! 1 document.

Luego desde otro cliente:

    xleo@client2:~$ lai --update
    Connecting to server..
    Updated! 1 document added.
    $ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

lai también soporta usuarios y permite compartir documentos entre ellos:

    xleo@client2:~$ lai --adduser 1 alfredo
    xleo@client1:~$ lai --commit
    Connecting to server..
    Commited! 1 document.

Luego el usuario alfredo descarga el documento compartido

    alfredo@client1:~$ lai --update
    Connecting to server..
    Updated! 1 document added.
    $ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

