#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import time

from tornado import web
from mongoengine import Q

from oauthserver.models.token import OAuthClient
from oauthserver.models.token import TokenApply
from oauthserver.views.base import BaseHandler
from oauthserver.config.settings import APPLY_STATUS

class AuthorizeTokenHandler(BaseHandler):
    @web.authenticated
    def get(self):
        role = self.get_secure_cookie("role")
        self.render('token.html', user=self.user, role = {"role": int(role)})

class AuthorizeTokenAjaxHandler(BaseHandler):
    @web.authenticated
    def get(self):
        info = {}
        token = OAuthClient.objects(member_id = self.user.member_id) .first()
        if token:
            info['authorize'] = 0
            info['key'] = token.client_key
            info['token'] = token.client_secret
            info['msg'] = u'your apply has been approved'
        else:
            apply_token = TokenApply.objects(member_id = self.user.member_id).first()
            if not apply_token:
                info['authorize'] = 1
            else:
                if apply_token.is_done:
                    info['msg'] = u'your apply has been refused'
                    info['authorize'] = 1
                else:
                    info['authorize'] = 2
                    info['apply_status'] = APPLY_STATUS[apply_token.apply_status]
        self.write(json.dumps({'info': info}))

    @web.authenticated
    def post(self):
        apply_token = TokenApply.objects(Q(member_id = self.user.member_id) & Q(apply_status = 0)).first()
        if apply_token:
            self.write(json.dumps({'errmsg': u'You have already applyed'}))
        else:
            description = self.get_argument("description", None)
            if not description:
                self.write(json.dumps({'errmsg': u'you need input reason for apply'}))
            else:
                new_apply = TokenApply()
                new_apply.name = self.user.name
                new_apply.member_id = self.user.member_id
                new_apply.description = description
                new_apply.apply_status = 0
                new_apply.save()
                self.write(json.dumps({'msg': u'your apply has been submited'}))


class AdminHandler(BaseHandler):
    @web.authenticated
    def get(self):
        if not self.is_admin:
            self.write("You aren't adminstrator")
        else:
            self.render("admin.html", user = self.user)

class AdminTokensAjaxHandler(BaseHandler):
    @web.authenticated
    def get(self):
        if not self.is_admin:
            raise web.HTTPError(404)
        offset = int(self.get_argument('offset', 1))
        total = len(TokenApply.objects)/20 if len(TokenApply.objects)%20 == 0 else len(TokenApply.objects)/20 + 1
        apply_tokens = TokenApply.objects(is_done = 0)\
                       .only("member_id", "name",
                             "description", "apply_status")[(offset - 1) * 10: offset+10]
        info = {}
        data = []
        for apply_token in apply_tokens:
            data.append({"name": apply_token.name, "member_id": apply_token.member_id,
                         "description": apply_token.description,
                         "apply_status": APPLY_STATUS[apply_token.apply_status],
                         'status': apply_token.apply_status})
        info['data'] = data
        info['page'] = offset
        info['totalpage'] = total
        self.write(json.dumps(info))

    @web.authenticated
    def post(self):
        member_id = self.get_argument("member_id", None)
        action = self.get_argument("action", None)
        if not member_id:
            raise web.HTTPError(404)
        if not action:
            raise web.HTTPError(404)
        apply_token = TokenApply.objects(Q(member_id = member_id) & Q(is_done = 0)).first()
        if not apply_token:
            raise web.HTTPError(404)
        action = action.strip()
        info = {'msg': ''}
        if action == 'pass':
            apply_token.apply_status = 1
            apply_token.is_done = 1
            apply_token.save()
            new_client = OAuthClient()
            new_client.member_id = apply_token.member_id
            new_client.set_client_secret()
            new_client.set_client_key()
            new_client.save()
            info['msg'] = u'this apply has been approved!'
        elif action == 'refuse':
            apply_token.apply_status = 2
            apply_token.is_done = 1
            apply_token.save()
            info['msg'] = u'this apply has been refused!'
        self.write(json.dumps(info))
