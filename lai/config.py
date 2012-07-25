SERVER = "http://localhost:8888"
USER = "lvidarte@gmail.com"
KEY_NAME = "howl"
#GITHUB_USER = "alfredormz"
#GITHUB_PASSWORD = "********"

DATABASE1 = {
    'ENGINE': 'mongo',
    'HOST'  : 'localhost',
    'PORT'  : 27017,
    'NAME'  : 'lai_dev',
    'TABLE' : '%s_%s' % ('xleo', 'client'),
}

DATABASE2 = {
    'ENGINE': 'sqlite',
    'NAME'  : 'lai.db',
    'TABLE' : '%s_%s' % (USER, 'client1'),
}

DATABASE = DATABASE1

