#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado import web
from oauthserver.models.token import OAuthClient

class BaseHandler(web.RequestHandler):
    def get_login_url(self):
        return self.reverse_url('login')

    @property
    def user(self):
        return self.get_current_user()

    def get_current_user(self):
        email = self.get_secure_cookie('email')
        if email:
            client = OAuthClient.objects(email = email).first()
            return client
        else:
            return None