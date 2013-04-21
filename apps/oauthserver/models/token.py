#!/usr/bin/env python
#-*-coding: utf8-*-

import time

from uuid import uuid4
from mongoengine import Document, StringField, IntField

class OAuthToken(Document):
    member_id = StringField(required = True, max_length = 40, unique = True)
    client_secret = StringField(required = True, max_length = 40)
    expire = IntField(required = True, default = 0)

    def set_client_secret(self):
        self.client_secret = uuid4().get_hex()

    def set_expire_time(self):
        self.expire = int(time.time()) + 30*24*3600

    meta = {
        'collection': 'oauthclient',
        'indexes': ['member_id', 'client_secret'],
        'shard_key': ('member_id',),
        'allow_inheritance': False
    }


class AccessToken(Document):
    member_id = StringField(required = True, max_length = 40, unique = True)
    access_token = StringField(required = True, max_length = 40)
    refresh_token = StringField(required = True, max_length = 40)
    expire = IntField(required = True, default = 0)
    refreshable = IntField(required = True, default = 1)

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
