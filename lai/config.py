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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

import os.path


SERVER_ADDR = "lai.calcifer.com.ar"
SERVER_PORT = 80
#USER = "lvidarte@gmail.com"
#KEY_NAME = "xleo@howl"
#GITHUB_USER = "lvidarte"
#GITHUB_PASSWORD = "********"

DATABASE1 = {
    'ENGINE': 'mongo',
    'HOST'  : 'localhost',
    'PORT'  : 27017,
    'NAME'  : 'lai_cli',
    'TABLE' : 'docs',
}

DATABASE2 = {
    'ENGINE': 'sqlite',
    'NAME'  : 'lai.db',
    'TABLE' : 'docs',
}

DATABASE = DATABASE1

SERVER_PUB_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEApJD544PRvoA1O7Mu6A73NHhQ24qxh5W++yqEbEzU+hN/YqB9rFG99lG/qhuhgYqvxo8OLBMsO72WoEPteHHeZ0UIgxiN4JOhQhcLgH9fghP46RyUGNYuRCKUdaq7+6L3WGJWj6GbwNJudDgdnJJD9pFnf25cSjqGSP/kLT2BRvLO1ZC/tUZJwpLtuPi9akpuwmlTBBXlroVzJNVe7W6w+3BGmodqQN4R0fVnSf2Hg8ZQhsGKzf/JGySATneTU5g144H/Z6ALHmBM6XqY0Ql3Crz2xSCTrIbEsvvS5WNlaoo+QTOKWD8YNRJ44u+xHSZFF1rM3E1f3L7DdFptIzcl2w== lvidarte@web199.webfaction.com'

CLIENT_PRV_KEY_PATH = os.path.join(os.path.expanduser('~'), ".ssh/id_rsa")
