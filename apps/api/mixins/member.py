#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

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

    def api_member_register(self, name, email, password):
        if not name:
            raise exceptions.ParamsException(u"missing name")
        if not email:
            raise exceptions.ParamsException(u"missing email")
        if not password:
            raise exceptions.ParamsException(u"missing password")
        member = Member.objects(email = email).first()
        if member:
            raise exceptions.BadRequest(u"email has been registerd")
        else:
            member = Member()
            member.name = name
            member.email = email
            member.set_password(password)
            member.generate_member_id()
            member.save()
            return {"success": True}

    def api_member_info(self):
        member = Member.objects(member_id = self.login_id).only("name").first()
        if member:
            return {"name": member.name}
        else:
            raise exceptions.InvalidRequest(u"no such user")