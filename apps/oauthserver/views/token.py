#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import time

from tornado import web
from models.token import AccessToken
from views.base import BaseHandler
from mongoengine import Q

from utils.tools import convert_time2days

class AuthorizeTokenHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render('token.html', user=self.user)

class AuthorizeTokenAjaxHandler(BaseHandler):
    @web.authenticated
    def get(self):
        info = {}
        token = AccessToken.objects(Q(member_id = self.user.member_id) & 
                                    Q(expire__gt = int(time.time()))) .first()
        if token:
            info['authorize'] = True
            info['token'] = token.access_token
            info['days'] = convert_time2days(int(time.time()), token.expire)
        else:
            info['authorize'] = False
        self.write(json.dumps({'info': info}))

    @web.authenticated
    def post(self):
        type = self.get_argument('type', None)
        if not type:
            self.write(json.dumps({'errmsg': u'invalid request'}))
        else:
            token = AccessToken.objects(member_id = self.user.member_id).first()
            if token:
                if type == 'update' and token.expire >= int(time.time()):
                    token.expire = int(time.time()) + 30*24*3600
                    token.save()
                    self.write(json.dumps({'msg': u'update success'}))
                elif type == 'delete':
                    #delete token
                    token.delete()
                    self.write(json.dumps({'msg': u'delete success'}))
                else:
                    self.write(json.dumps({'errmsg': u'bad request'}))
            elif not token and type == 'add':
                newtoken = AccessToken()
                newtoken.member_id = self.user.member_id
                newtoken.set_access_token()
                newtoken.set_refresh_token()
                newtoken.set_expire_time()
                newtoken.save()
                self.write(json.dumps({'msg': u'create token success'}))

