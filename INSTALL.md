# Clone github repository

    $ git clone git@github.com:lvidarte/lai-client.git

# Create env

    $ cd lai-client
    $ ./bin/create_env.sh

This will install the required packages argparse and pycrypto
    

# Packages

## Required

 * argparse==1.2.1
 * pycrypto==2.6

## Optionals

 * pymongo==2.2 or MySQL-python==1.2.4 (default is sqlite3)
 * clint==0.3.1 (for colored ouput)
 * PyGithub==1.8.0 (to send gists to github)
 * gtk or PyQt4 or xclip (for copy to clipboard)

## To Install all packages

    $ source env/bin/activate
    $ pip install -r requirements.txt

# Environment variables

Set the following bash variables

    export LAI_ENV_PATH=/path/to/virtualenv
    export LAI_MODULE_PATH=/path/to/module/lai

Finally run lai with lai-client script

    $ bin/lai-client
