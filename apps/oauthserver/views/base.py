#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado import web
from oauthserver.models.member import Member

class BaseHandler(web.RequestHandler):
    def get_login_url(self):
        return self.reverse_url('login')

    @property
    def user(self):
        return self.get_current_user()

    def get_current_user(self):
        user_id = self.get_secure_cookie('user_id')
        if user_id:
            user = Member.objects(member_id=user_id).first()
            return user
        else:
            return None