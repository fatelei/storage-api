#!/usr/bin/env python
#-*-coding: utf8-*-

from mongoengine import connect
from oauthserver.models.token import OAuthMember
from base_config import MONGODB

def run():
    connect(db = MONGODB['db'], host = MONGODB['host'], port = MONGODB['port'])
    admin = OAuthMember()
    admin.email = "fatelei@gmail.com"
    admin.set_password("123456")
    admin.set_member_id()
    admin.name = "admin"
    admin.role = 1
    admin.save()

if __name__ == '__main__':
    run()