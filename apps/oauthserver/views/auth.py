#!/usr/bin/env python
#-*-coding: utf8-*-

import logging
import json

from tornado import web
from base import BaseHandler
from oauthserver.models.member import Member
from oauthserver.utils.macro import HTTP_CODE
from oauthserver.utils import exceptions
from oauthserver.utils.validate import TokenGenerator

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
            member = Member.objects(name=name, email=email).first()
            if member:
                err['msg'] = u"该用户已被注册"
                self.render('register.html', err=err)
            else:
                member = Member(name=name, email=email)
                member.set_password(password)
                member.generate_member_id()
                member.save()
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
        member = Member.objects(email = email).first()
        if member and member.check_password(password):
            self.set_secure_cookie('user_id', member.member_id)
            self.redirect(self.reverse_url('token'))
        else:
            err['msg'] = u'poassword is invalid'
            self.render('login.html', err=err)



class OAuthLogoutHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.clear_cookie('user_id')
        self.redirect(self.reverse_url('login'))


class OAuthForApiHandler(BaseHandler):
    def post(self):
        try:
            token_generator = TokenGenerator(self)
            token_generator.validate()
            info = token_generator.grant_response()
        except exceptions.OAuthException, e:
            info = e.info
            self.set_status(HTTP_CODE.UNAUTHORIZED)
        except Exception, e:
            logging.warning(e, exc_info = True)
            info = exceptions.ServerError().info
            self.set_status(HTTP_CODE.INTERNAL_SERVER_ERROR)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(info))

