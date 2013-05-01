#!/usr/bin/env python
#-*-coding: utf8-*-

import logging
import json

from tornado import web
from base import BaseHandler
from oauthserver.models.token import OAuthMember

class OAuthRegisterHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect(self.reverse_url('token'))
        else:
            self.render('register.html', err={})

    def post(self):
        name = self.get_argument('username', None)
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)
        err = {'msg': ''}
        if not name or not email or not password:
            err['msg'] = u"name or email or password can't be blank"
            self.render('register.html', err=err)
        else:
            client = OAuthMember.objects(name=name, email=email).first()
            if client:
                err['msg'] = u"该用户已被注册"
                self.render('register.html', err=err)
            else:
                client = OAuthMember(name=name, email=email)
                client.set_password(password)
                client.set_member_id()
                client.save()
                self.redirect(self.reverse_url('login'))


class OAuthLoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect(self.reverse_url('token'))
        else:
            self.render('login.html', err={})

    def post(self):
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)
        err = {'msg': ''}
        if not email and not password:
            err['msg'] = u"email or password can't be blank"
            self.render('login.html', err=err)
        client = OAuthMember.objects(email = email).first()
        if client and client.check_password(password):
            self.set_secure_cookie('email', client.email)
            self.set_secure_cookie('role', str(client.role))
            if client.role == 0:
                self.redirect(self.reverse_url('token'))
            else:
                self.redirect(self.reverse_url('admin'))
        else:
            err['msg'] = u'poassword is invalid'
            self.render('login.html', err=err)


class OAuthLogoutHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.clear_all_cookies()
        self.redirect(self.reverse_url('login'))


