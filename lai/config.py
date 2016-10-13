# -*- coding: utf-8 -*-

# Author: Leo Vidarte <http://nerdlabs.com.ar>
#
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

import os
import sys


SERVER_ADDR = "lai.nerdlabs.com.ar"
SERVER_PORT = 80
USER = ""
KEY_NAME = ""
PRV_KEY_PATH = os.path.join(os.path.expanduser('~'), ".ssh/id_rsa")

GITHUB_USER = ""
GITHUB_PASSWORD = ""

database = {
    'engine': 'sqlite',
    'name'  : 'data/lai.db',
}


SERVER_PUB_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEApJD544PRvoA1O7Mu6A73NHhQ24qxh5W++yqEbEzU+hN/YqB9rFG99lG/qhuhgYqvxo8OLBMsO72WoEPteHHeZ0UIgxiN4JOhQhcLgH9fghP46RyUGNYuRCKUdaq7+6L3WGJWj6GbwNJudDgdnJJD9pFnf25cSjqGSP/kLT2BRvLO1ZC/tUZJwpLtuPi9akpuwmlTBBXlroVzJNVe7W6w+3BGmodqQN4R0fVnSf2Hg8ZQhsGKzf/JGySATneTU5g144H/Z6ALHmBM6XqY0Ql3Crz2xSCTrIbEsvvS5WNlaoo+QTOKWD8YNRJ44u+xHSZFF1rM3E1f3L7DdFptIzcl2w== lvidarte@web199.webfaction.com'


try:
    from local_config import *
except:
    pass


if USER == "" or KEY_NAME == "":
    try:
        USER = os.environ["USER"]
        KEY_NAME = os.environ["KEY_NAME"]
    except:
        print "Error: USER and KEY_NAME must be defined."
        sys.exit(1)

if GITHUB_USER == "" or GITHUB_PASSWORD == "":
    try:
        GITHUB_USER = os.environ["GITHUB_USER"]
        GITHUB_PASSWORD = os.environ["GITHUB_PASSWORD"]
    except:
        GITHUB_USER = ""
        GITHUB_PASSWORD = ""

