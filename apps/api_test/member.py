#!/usr/bin/env python
#-*-coding: utf8-*-

import unittest
import config

from core.member import Member
from core.base import StorageOAuthClient

class TestMember(unittest.TestCase):
    def setUp(self):
        self.email = config.EMAIL
        self.password = config.PASSWORD        
        self.token = config.TOKEN
        self.client_secret = config.CLIENT_SECRET
        self.oauth = StorageOAuthClient(oauth_url = config.OAUTH_URL, email = self.email,
                                        password = self.password, client_secret = self.client_secret)
        self.member = Member(api_url = config.API_URL, token = self.token)

    def test_login(self):
        resp, content = self.oauth.basic_login()
        print content
        self.assertEqual(int(resp['status']), 200)

    def test_pwd_change(self):
        params = {"password": "123456", "re_password": "123456"}
        resp, content = self.member.change_password(**params)
        self.assertEqual(int(resp['status']), 200)

if __name__ == '__main__':
    testsuite = unittest.TestLoader().loadTestsFromTestCase(TestMember)
    unittest.TextTestRunner(verbosity = 2).run(testsuite)