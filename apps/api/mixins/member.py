#!/usr/bin/env python
#-*-coding: utf8-*-

from oauthserver.models.member import Member
from api.allin import exceptions

class MemberMixin(object):
    def api_member_change_password(self, password, re_password):
        if not password or not re_password:
            raise exceptions.InvalidRequest('params error')
        if password != re_password:
            raise exceptions.InvalidRequest('password is not the same')
        member = Member.objects(member_id = self.login_id).first()
        if not member:
            raise exceptions.InvalidRequest('you need login first')
        member.set_password(password)
        member.save()
        return {'success': True}