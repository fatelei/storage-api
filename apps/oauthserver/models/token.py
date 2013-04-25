#!/usr/bin/env python
#-*-coding: utf8-*-

import time

from uuid import uuid4
from mongoengine import Document, StringField, IntField
from hashlib import sha1
from struct import pack
from random import getrandbits

class OAuthClient(Document):
    name = StringField(required = True, max_length = 40, unique = True)
    email = StringField(required = True, max_length = 40, unique = True)
    password = StringField(required = True, max_length = 40)
    client_key = StringField(max_length = 40, default = None)
    client_secret = StringField(max_length = 40, default = None)
    expire = IntField(required = True, default = 0)

    def encryption(self, password):
        if isinstance(password, unicode):
            password = password.encode('utf8')
        salt = pack('I', getrandbits(32))
        digest = sha1(password + salt).digest()
        return (salt + digest).encode('base64')

    def set_password(self, password):
        self.password = self.encryption(password)

    def check_password(self, password):
        if isinstance(password, unicode):
            password = password.encode('utf8')
        old_password = self.password.decode('base64')
        if len(old_password) != 24:
            return False
        salt = old_password[:4]
        digest = old_password[4:]
        if digest != sha1(password + salt).digest():
            return False
        return True

    def set_client_key(self):
        self.client_key = uuid4().get_hex()

    def set_client_secret(self):
        self.client_secret = uuid4().get_hex()

    def set_expire_time(self):
        self.expire = int(time.time()) + 30*24*3600

    meta = {
        'collection': 'oauthclient',
        'indexes': ['email', 'client_key', 'client_secret'],
        'shard_key': ('email',),
        'allow_inheritance': False
    }


class AccessToken(Document):
    member_id = StringField(required = True, max_length = 40)
    access_token = StringField(required = True, max_length = 40)
    refresh_token = StringField(required = True, max_length = 40)
    expire = IntField(required = True, default = 0)
    refreshable = IntField(required = True, default = 1)
    is_expired = IntField(default = 0)

    def set_access_token(self):
        self.access_token = uuid4().get_hex()

    def set_refresh_token(self):
        self.refresh_token = uuid4().get_hex()

    def set_expire_time(self):
        self.expire = int(time.time()) + 30*24*3600

    meta = {
        'collection': 'accesstoken',
        'indexes': ['member_id', 'access_token', 'refresh_token'],
        'shard_key': ('member_id',),
        'allow_inheritance': False
    }
