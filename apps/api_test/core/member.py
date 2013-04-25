#!/usr/bin/env python
#-*-coding: utf8-*-

from base import StorageAPIClient

class Member(StorageAPIClient):
    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)

    def change_password(self, **params):
        return self.put("member/pwdchange", **params)


