#!/usr/bin/env python
#-*-coding: utf8-*-

from demo.views.base import BaseHandler
from demo.settings import CORRECT_HTTP_CODE

class DemoLoginHandler(BaseHandler):
    def get(self):
        token = self.get_secure_cookie("access_token")
        if token:
            pass
        else:
            self.render("login.html", err = {})

    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        err = {'msg': ''}
        if not email:
            err['msg'] = u'no email'
            self.render("login.html", err = err)
        if not password:
            err['msg'] = u'no password'
            self.render("login.html", err = err)
        data = {"email": email, "password": password}
        resp, content = self.client.oauth_login(data)
        if int(resp['status']) in CORRECT_HTTP_CODE:
            self.set_secure_cookie("access_token", content['access_token'])
            self.set_secure_cookie("name", content["name"])
        else:
            self.render("login.html", err = content)

class DemoLogoutHandler(BaseHandler):
    def post(self):
        pass

class DemoRegisterHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        pass

class DemoPwdChange(BaseHandler):
    def get(self):
        pass

    def post(self):
        pass