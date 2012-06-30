SERVER = "http://localhost:8888"

USER = "xleo"

DATABASE1 = {
    'ENGINE': 'mongo',
    'HOST'  : 'localhost',
    'PORT'  : 27017,
    'NAME'  : 'lai',
    'TABLE' : '%s_%s' % (USER, 'client1'),
}

DATABASE2 = {
    'ENGINE': 'sqlite',
    'NAME'  : 'lai.db',
    'TABLE' : '%s_%s' % (USER, 'client1'),
}

DATABASE = DATABASE1

