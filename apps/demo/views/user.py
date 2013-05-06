#!/usr/bin/env python
#-*-coding: utf8-*-

import logging
import json

from tornado import web

from demo.views.base import BaseHandler
from demo.utils.tools import check_status

class DemoLoginHandler(BaseHandler):
    def get(self):
        token = self.get_secure_cookie("access_token")
        if token:
            self.redirect(self.reverse_url("index"))
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
        status, content = self.client.oauth_login(**data)
        content = json.loads(content)
        if "error" in content:
            err['msg'] = content['error']['message']
            self.render("login.html", err = err)
        if check_status(int(status['status'])):
            self.set_secure_cookie("access_token", content['access_token'])
            self.redirect(self.reverse_url("index"))
        else:
            err['msg'] = content['error']['message']
            self.render("login.html", err = err)

class DemoLogoutHandler(BaseHandler):
    @web.authenticated
    def get(self):
        token = self.get_secure_cookie("access_token")
        data = {"access_token": token}
        resp, content = self.client.oauth_logout(**data)
        if check_status(int(resp['status'])):
            self.clear_all_cookies()
            self.redirect(self.reverse_url("login"))
        else:
            self.write(content)

class DemoRegisterHandler(BaseHandler):
    def get(self):
        token = self.get_secure_cookie("access_token")
        if token:
            self.redirect(self.reverse_url("index"))
        else:
            self.render("register.html", err = {})

    def post(self):
        name = self.get_argument("name", None)
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        err = {'msg': ''}
        if not name:
            err['msg'] = u'missing name'
            self.render("register.html", err = err)
        if not email:
            err['msg'] = u'missing email'
            self.render("register.html", err = err)
        if not password:
            err['msg'] = u'missing password'
            self.render("register.html", err = err)
        data = {'name': name, 'email': email, 'password': password}
        resp, content = self.client.oauth_register(**data)
        content = json.loads(content)
        if check_status(int(resp['status'])):
            self.redirect(self.reverse_url("login"))
        else:
            err['msg'] = content['error']['message']
            self.render("register.html", err = err)

class DemoPwdChangeHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render("pwdchange.html", err = {})

    @web.authenticated
    def post(self):
        password = self.get_argument("password", None)
        re_password = self.get_argument("re_password", None)
        err = {'msg': ''}
        if password != re_password:
            err['msg'] = u"password isn't the same"
            self.render("pwdchange.html", err = err)
        else:
            data = {'password': password, 're_password': re_password}
            resp, content = self.client.api_put("member/pwdchange", **data)
            content = json.loads(content)
            if check_status(int(resp['status'])):
                self.render("pwdchange.html", err = content)
            else:
                err['msg'] = content['error']['message']
                self.render("pwdchange.html", err = err)