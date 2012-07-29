# -*- coding: utf-8 -*-

# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8888
USER = "lvidarte@gmail.com"
KEY_NAME = "howl"
#GITHUB_USER = "lvidarte"
#GITHUB_PASSWORD = "********"

DATABASE1 = {
    'ENGINE': 'mongo',
    'HOST'  : 'localhost',
    'PORT'  : 27017,
    'NAME'  : 'lai_cli_dev',
    'TABLE' : 'docs',
}

DATABASE2 = {
    'ENGINE': 'sqlite',
    'NAME'  : 'lai.db',
    'TABLE' : '%s_%s' % (USER, 'client1'),
}

DATABASE = DATABASE1

