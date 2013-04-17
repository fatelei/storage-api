#!/usr/bin/env python
#-*-coding: utf8-*-

from base import BaseHandler
from api.allin import exceptions
from api.mixinx.member import MemberMixin


class MemberPwdChange(BaseHandler, MemberMixin):
    def real_put(self, *arge, **kwargs):
        password = self.get_argument('password', None)
        re_password = self.get_argument('re_password', None)
        info = self.api_member_change_password(password, re_password)
        return info