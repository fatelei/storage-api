#!/usr/bin/env python
#-*-coding: utf8-*-

from uuid import uuid4
from mongoengine import Document, StringField, EmailField
from hashlib import sha1
from struct import pack
from random import getrandbits

class Member(Document):
    member_id = StringField(max_length=40, required=True)
    name = StringField(max_length=40, required=True, unique=True)
    password = StringField(max_length=40, required=True)
    email = EmailField(required=True, unique=True)

    meta = {
        'collection': 'member',
        'allow_inheritance': False,
        'indexes': ['member_id', 'name', 'email'],
        'shard_key': ('member_id', 'email')
    }

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

    def generate_member_id(self):
        self.member_id = uuid4().get_hex()

