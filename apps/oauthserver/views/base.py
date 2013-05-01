#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado import web
from oauthserver.models.token import OAuthMember

class BaseHandler(web.RequestHandler):
    def get_login_url(self):
        return self.reverse_url('login')

    @property
    def is_admin(self):
        role = self.get_secure_cookie('role')
        if not role:
            return False
        else:
            if int(role) == 0:
                return False
            elif int(role) == 1:
                return True
            else:
                return False

    @property
    def user(self):
        return self.get_current_user()

    def get_current_user(self):
        email = self.get_secure_cookie('email')
        if email:
            client = OAuthMember.objects(email = email).first()
            return client
        else:
            return None