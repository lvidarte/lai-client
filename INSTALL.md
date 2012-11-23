# 1. Clone github repository

    $ git clone git@github.com:lvidarte/lai-client.git

# 2. Create virtualenv

    $ cd lai-client
    $ ./bin/create_env.sh

This will install the required packages argparse and pycrypto

## Packages

### Required

 * argparse==1.2.1
 * pycrypto==2.6

### Optionals

 * pymongo==2.2 or MySQL-python==1.2.4 (default is sqlite3)
 * clint==0.3.1 (for colored ouput)
 * PyGithub==1.8.0 (to send gists to github)
 * gtk or PyQt4 or xclip (for copy to clipboard)

To Install all packages

    $ source env/bin/activate
    $ pip install -r requirements.txt

# 3. Set bash variables

Put the following in your .bashrc

    export LAI_ENV_PATH=/path/to/virtualenv
    export LAI_MODULE_PATH=/path/to/module/lai

Finally run lai with lai-client script

    $ bin/lai-client

# 4. Other settings

## a. Set your user and key name to connect with lai-server

First login into http://lai.calcifer.com.ar with your Google account.
Then upload your public key and set a name to identify it.
Finally create the lai/local_config.py file and set the following

    USER = "your-username@gmail.com"
    KEY_NAME = "name_of_your_public_key"

## b. Setting database

### The default database engine in Lai is Sqlite3

    DATABASE = {'ENGINE': 'sqlite',
                'NAME'  : '/path/to/lai.db'}

### MongoDB

Install the pymongo package

    source env/bin/activate
    pip install pymongo==2.2

To use mongodb set into lai/local_config.py

    DATABASE = {'ENGINE': 'mongo',
                'HOST'  : 'localhost',
                'PORT'  : 27017,
                'NAME'  : 'lai_client'}

### MySQL

Install the MySQL-python package

    source env/bin/activate
    pip install MySQL-python==1.2.4c1

To user mysql set into lai/local_config.py

    DATABASE = {'ENGINE': 'mysql',
                'HOST'  : 'localhost',
                'PORT'  : 3306,
                'USER'  : 'username',
                'PASSWD': 'passwd',
                'NAME'  : 'db-name'}

## c. Setting Github

Install the PyGithub module

    source env/bin/activate
    pip install PyGithub==1.8.0

Put the following into lai/local_config.py

    GITHUB_USER = 'your-username'
    GITHUB_PASSWORD = 'your-passwd'

## d. Use the lai shell

    $ ./shell.py 
    Python 2.7.2+ (default, Jul 20 2012, 22:12:53) 
    Welcome to lai shell
    Autocompletion and history are enabled
    
    Lai objects:
        config    (module)  from lai import config
        Database  (class)   from lai import Database
        Client    (class)   from lai import Client
        Document  (class)   from lai import Document
        database  (object)  database = Database()
        client    (object)  client = Client(database)
    
    >>> for doc in client.search('apache'):
    ...     print doc.data.content
    ... 
    ps -ef | awk '!/awk/&&/sbin\/apache/' | wc -l
    apache2ctl status
    apache2ctl configtest
    zabbix: zabbix_get -s192.168.12.138 -p10050 -k"proc.num[apache2]"
    update-rc.d apache2 defaults 20 80
    >>> 


    
