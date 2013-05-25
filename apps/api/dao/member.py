#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

from mongoengine import Q

from oauthserver.models.member import Member
from api.allin import exceptions

class MemberDAO(object):
    @classmethod
    def member_passwd_change(cls, password, re_password, member_id):
        member = Member.objects(member_id = member_id).first()
        if not member:
            raise exceptions.InvalidRequest('请先登陆')
        member.set_password(password)
        member.save()
        return {'success': True}

    @classmethod
    def member_register(cls, name, email, password):
        member = Member.objects(Q(email = email) | Q(name = name)).first()
        if member:
            raise exceptions.BadRequest(u"该用户已经被注册")
        else:
            member = Member()
            member.name = name
            member.email = email
            member.set_password(password)
            member.generate_member_id()
            member.save()
            return {"success": True}

    @classmethod
    def member_info(cls, member_id):
        member = Member.objects(member_id = member_id).only("name").first()
        if member:
            return {"name": member.name}
        else:
            raise exceptions.InvalidRequest(u"不存在此用户")

    @classmethod
    def search_member(cls, member_id):
        members = Member.objects(member_id__ne = member_id).only("name")
        names = []
        for member in members:
            names.append(member.name)
        return names