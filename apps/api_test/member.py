#!/usr/bin/env python
#-*-coding: utf8-*-

import unittest
import config
import requests
import urllib

from core.utils import urlencode
from core.member import Member
from core.base import StorageOAuthClient

class TestMember(unittest.TestCase):
    def setUp(self):
        self.email = config.EMAIL
        self.password = config.PASSWORD        
        self.token = config.TOKEN
        self.client_secret = config.CLIENT_SECRET
        self.client_key = config.CLIENT_KEY
        self.oauth = StorageOAuthClient(oauth_url = config.LOGIN_URL, email = self.email,
                                        password = self.password, client_secret = self.client_secret, client_key = self.client_key)
        self.member = Member(api_url = config.API_URL, token = self.token)

    @unittest.skip("skip")
    def test_login(self):
        resp, content = self.oauth.basic_login()
        self.assertEqual(int(resp['status']), 200)

    
    def test_pwd_change(self):
        params = {"password": "123456", "re_password": "123456"}
        resp, content = self.member.change_password(**params)
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_member_logout(self):
        logout_url = "%s/member/logout/%s" % (config.API_URL, self.token)
        resp, content = self.oauth.basic_logout(logout_url)
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_member_register(self):
        register_url = '%s/member/register' % (config.API_URL)
        post_data = {"name": "test12", "email": "test1@test1.com", "password": "123456"}
        body = urlencode(post_data)
        headers = {"Authorization": "oauth:%s" % config.CLIENT_KEY, "Content-type": "application/x-www-form-urlencoded"}
        response = requests.post(register_url, data = body, headers = headers, verify = False)
        status = response.status_code
        self.assertEqual(status, 200)

if __name__ == '__main__':
    testsuite = unittest.TestLoader().loadTestsFromTestCase(TestMember)
    unittest.TextTestRunner(verbosity = 2).run(testsuite)