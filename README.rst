lai
===

Es un programa de línea de comandos que permite guardar anotaciones y mantenerlas sincronizadas entre varias computadoras. La idea es guardarte comandos, shortcuts, snippets y en gral cualquier cosa que quieras tener a mano en la consola. También podés compartir documentos con otros usuarios::

    juan@compu1:~$ lai --add 'git fetch origin [remote-branch]:[new-local-branch]'

Luego, al buscar por 'git' (por defecto lai busca)::

    juan@compu1:~$ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

También podés traer el documento por su id::

    juan@compu1:~$ lai --get 1
    git fetch origin [remote-branch]:[new-local-branch]

Como lai trabaja en modo cliente-servidor podés tener varios clientes sincronizados contra un servidor central, todo mediante un simple sync::

    juan@compu1:~$ lai --sync

Luego desde otro cliente::

    juan@client2:~$ lai --sync
    juan@client2:~$ lai git
    1: git fetch origin [remote-branch]:[new-local-branch]

lai permite que guardes tus documentos como públicos o privados. Si compartís un servidor lai podés buscar entre los documentos públicos de otros usuarios y copiar a tu cuenta los que quieras::

    javier@client3:~$ lai --public-search git
    500230da304297180d207d4b: git fetch origin [remote-branch]:[new-local-branch]
    javier@client3:~$ lai --copy 500230da304297180d207d4b

