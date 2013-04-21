#!/usr/bin/env python
#-*-coding: utf8-*-

import ujson

from tornado.web import RequestHandler
from tornado.options import options

from oauthserver.models.member import Member
from api.utils.auth import Authenticator
from api.utils.decorator import ExceptionHandler
from api.allin import exceptions
from api.allin.macro import HTTP_CODE


class BaseHandler(RequestHandler, Authenticator):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def login_id(self):
        return self.current_user.member_id if self.current_user else None

    def current_user(self):
        if self.st_member_id:
            member = Member.objects(member_id = self.st_member_id).first()
            return member
        else:
            return None

    def prepare(self):
        try:
            self.auth_info = self.validate()
        except exceptions.StorageOauthException, e:
            self.set_status(HTTP_CODE.UNAUTHORIZED)
            self.finish(ujson.dumps(e.info))
        self.st_member_id = self.auth_info['member_id']

    def finish(self, chunk = None):
        self._chunk = chunk
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        RequestHandler.finish(self, self._chunk)

    @ExceptionHandler
    def get(self, *args, **kwargs):
        return self.real_get(*args, **kwargs)

    @ExceptionHandler
    def post(self, *args, **kwargs):
        return self.real_post(*args, **kwargs)

    @ExceptionHandler
    def put(self, *args, **kwargs):
        return self.real_put(*args, **kwargs)

    @ExceptionHandler
    def delete(self, *args, **kwargs):
        return self.real_delete(*args, **kwargs)

    @ExceptionHandler
    def options(self, *args, **kwargs):
        return self.real_options(*args, **kwargs)


