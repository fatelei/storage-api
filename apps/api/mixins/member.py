#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

from oauthserver.models.member import Member
from api.dao.member import MemberDAO
from api.allin import exceptions

class MemberMixin(object):
    def api_member_change_password(self, password, re_password):
        info = MemberDAO.member_passwd_change(password, re_password, self.login_id)
        return info

    def api_member_register(self, name, email, password):
        info = MemberDAO.member_register(name, email, password)
        return info

    def api_member_info(self):
        info = MemberDAO.member_info(self.login_id)
        return info

    def api_search_member(self):
        info = MemberDAO.search_member(self.login_id)
        return info