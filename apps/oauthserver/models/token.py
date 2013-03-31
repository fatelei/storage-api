#!/usr/bin/env python
#-*-coding: utf8-*-

import time

from uuid import uuid4
from mongoengine import Document, StringField, IntField

class AccessToken(Document):
    member_id = StringField(required=True, max_length=40)
    access_token = StringField(required=True, max_length=40)
    expire = IntField(required=True, default=0)

    def set_access_token(self):
        self.access_token = uuid4().get_hex()

    def set_expire_time(self):
        self.expire = int(time.time()) + 30*24*3600

    meta = {
        'collection': 'oauth_accesstoken',
        'index': ['member_id', 'access_token'],
        'shard_key': ('member_id',),
        'allow_inheritance': False
    }

