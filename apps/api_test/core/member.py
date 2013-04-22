#!/usr/bin/env python
#-*-coding: utf8-*-

class MemberTestMixin(StorageAPIClient, StorageOAuthClient):
    def test_basic_login(self, email, password, client_secret):
        