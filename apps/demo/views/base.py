#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.web import RequestHandler

from demo.utils.client import APIClient

class BaseHandler(RequestHandler):
    def get_login_url(self):
        return self.reverse_url('login')
        
    def get_current_user(self):
        token = self.get_secure_cookie("access_token")
        if token:
            return token
        else:
            return None

    def prepare(self):
        self.client = APIClient()