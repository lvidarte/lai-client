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
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto import Random
import cStringIO
import struct


PASSWD_SIZE = 32
CHUNK_SIZE = 64 * 1024
ERROR = '_DECRYPT_ERROR_'


def encrypt(message, public_key):
    key = RSA.importKey(public_key)
    pkcs1_encryptor = PKCS1_v1_5.new(key)

    passwd = os.urandom(PASSWD_SIZE)
    iv = Random.new().read(AES.block_size)
    aes_encryptor = AES.new(passwd, AES.MODE_CBC, iv)
    passwd_encrypted = pkcs1_encryptor.encrypt(passwd)

    data = cStringIO.StringIO()
    data.write(struct.pack('<Q', len(passwd_encrypted)))
    data.write(passwd_encrypted)
    data.write(iv)
    while len(message) > 0:
        chunk = message[0:CHUNK_SIZE]
        message = message[CHUNK_SIZE:]
        if len(chunk) % 16 != 0:
            chunk += ' ' * (16 - len(chunk) % 16)
        data.write(aes_encryptor.encrypt(chunk))
    return data.getvalue()

def decrypt(data, private_key):
    data = cStringIO.StringIO(data)

    key = RSA.importKey(private_key)
    pkcs1_decryptor = PKCS1_v1_5.new(key)

    passwd_size = long(struct.unpack('<Q', data.read(struct.calcsize('Q')))[0])
    passwd_encrypted = data.read(passwd_size)
    passwd = pkcs1_decryptor.decrypt(passwd_encrypted, ERROR)

    if passwd == ERROR:
        raise Exception('Private key error')

    iv = data.read(16)
    aes_decryptor = AES.new(passwd, AES.MODE_CBC, iv)
    message = str()
    while True:
        chunk = data.read(CHUNK_SIZE)
        if len(chunk) == 0:
            break
        message += aes_decryptor.decrypt(chunk)
    return message


if __name__ == '__main__':
    import os.path
    public_key = os.path.join(os.path.expanduser('~'), ".ssh/id_rsa.pub")
    public_key = open(public_key).read()
    message = "hello fucking world " * 50
    print "len message %d" % len(message)
    data = encrypt(message, public_key)
    print "len data encrypted %d" % len(data)
    private_key = os.path.join(os.path.expanduser('~'), ".ssh/id_rsa")
    private_key = open(private_key).read()
    print decrypt(data, private_key)
