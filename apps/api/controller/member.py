#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import logging

from tornado import web
from mongoengine import Q

from api.controller.base import BaseHandler
from api.allin import exceptions
from api.mixins.member import MemberMixin

from oauthserver.utils.validate import TokenGenerator
from oauthserver.utils.macro import HTTP_CODE
from oauthserver.utils import exceptions
from oauthserver.models.token import AccessToken


class MemberPwdChange(BaseHandler, MemberMixin):
    def real_put(self, *arge, **kwargs):
        password = self.get_argument('password', None)
        re_password = self.get_argument('re_password', None)
        if not password or not re_password:
            raise exceptions.InvalidRequest(u'参数错误')
        if password != re_password:
            raise exceptions.InvalidRequest(u'密码不一致')
        info = self.api_member_change_password(password, re_password)
        return info

class OAuthApiLoginHandler(web.RequestHandler):
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
        logging.warning(info)
        self.write(json.dumps(info))

class OAuthApiLogoutHandler(web.RequestHandler):
    def post(self, access_token):
        token = AccessToken.objects(Q(access_token = access_token) & Q(is_expired = 0)).first()
        if token:
            token.is_expired = 1
            token.refreshable = 0
            token.save()
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps({"success": True}))
        else:
            raise exceptions.InvalidRequest(u"用户已经注销")

class RegisterHandler(BaseHandler, MemberMixin):
    def real_post(self):
        name = self.get_argument("name", None)
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        if not name:
            raise exceptions.ParamsException(u"请输入用户名")
        if not email:
            raise exceptions.ParamsException(u"请输入注册邮箱")
        if not password:
            raise exceptions.ParamsException(u"请输入注册密码")
        info = self.api_member_register(name, email, password)
        return info

class MemberInfoHandler(BaseHandler, MemberMixin):
    def real_get(self):
        info = self.api_member_info()
        return info

class MemberSearchHandler(BaseHandler, MemberMixin):
    def real_get(self):
        info = self.api_search_member()
        return info