#!/usr/bin/env python
#-*-coding: utf8-*-

import logging
import json

from tornado import web
from base import BaseHandler
from oauthserver.models.token import OAuthClient

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
            client = OAuthClient.objects(name=name, email=email).first()
            if client:
                err['msg'] = u"该用户已被注册"
                self.render('register.html', err=err)
            else:
                client = OAuthClient(name=name, email=email)
                client.set_password(password)
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
        client = OAuthClient.objects(email = email).first()
        if client and client.check_password(password):
            self.set_secure_cookie('email', client.email)
            self.redirect(self.reverse_url('token'))
        else:
            err['msg'] = u'poassword is invalid'
            self.render('login.html', err=err)



class OAuthLogoutHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.clear_cookie('email')
        self.redirect(self.reverse_url('login'))


