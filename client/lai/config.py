SERVER = "http://localhost:8888"
USER = "alfredormz"
GITHUB_USER = "alfredormz"
GITHUB_PASSWORD = "********"

DATABASE1 = {
    'ENGINE': 'mongo',
    'HOST'  : 'localhost',
    'PORT'  : 27017,
    'NAME'  : 'lai',
    'TABLE' : '%s_%s' % (USER, 'client2'),
}

DATABASE2 = {
    'ENGINE': 'sqlite',
    'NAME'  : 'lai.db',
    'TABLE' : '%s_%s' % (USER, 'client1'),
}

DATABASE = DATABASE2

