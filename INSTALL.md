# Clone github repository

    $ git clone git@github.com:lvidarte/lai-client.git

# Create env

    $ cd lai-client
    $ ./bin/create_env.sh

This will install the required packages argparse and pycrypto

# Packages

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

# Set the following bash variables

    export LAI_ENV_PATH=/path/to/virtualenv
    export LAI_MODULE_PATH=/path/to/module/lai

Finally run lai with lai-client script

    $ bin/lai-client

# Set your user and key_name

First login into http://lai.calcifer.com.ar with your Google account.
Then upload your public key and set a name to identify it.
Finally create the lai/local_config.py file and set the following

    USER = "your-username@gmail.com"
    KEY_NAME = "name_of_your_public_key"

# The default database engine in Lai is sqlite3

    DATABASE = {'ENGINE': 'sqlite',
                'NAME'  : '/home/your-username/lai.db'}

# To use mongodb set into lai/local_config.py

    DATABASE = {'ENGINE': 'mongo',
                'HOST'  : 'localhost',
                'PORT'  : 27017,
                'NAME'  : 'lai_client'}

# To user mysql set into lai/config.py

    DATABASE = {'ENGINE': 'mysql',
                'HOST'  : 'localhost',
                'PORT'  : 3306,
                'USER'  : 'username',
                'PASSWD': 'passwd',
                'NAME'  : 'db-name'}

