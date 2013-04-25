#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import time

from tornado import web
from mongoengine import Q

from oauthserver.models.token import OAuthClient
from oauthserver.views.base import BaseHandler
from oauthserver.utils.tools import convert_time2days

class AuthorizeTokenHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render('token.html', user=self.user)

class AuthorizeTokenAjaxHandler(BaseHandler):
    @web.authenticated
    def get(self):
        info = {}
        token = OAuthClient.objects(Q(email = self.user.email) & 
                                    Q(expire__gt = int(time.time()))) .first()
        if token:
            info['authorize'] = True
            info['key'] = token.client_key
            info['token'] = token.client_secret
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
            token = OAuthClient.objects(email = self.user.email).first()
            if token:
                if type == 'update' and token.expire >= int(time.time()):
                    token.expire = int(time.time()) + 30*24*3600
                    token.save()
                    self.write(json.dumps({'msg': u'update success'}))
                elif type == 'delete':
                    #delete token
                    token.delete()
                    self.write(json.dumps({'msg': u'delete success'}))
                elif type == 'add':
                    token.set_client_secret()
                    token.set_client_key()
                    token.set_expire_time()
                    token.save()
                    self.write(json.dumps({'msg': u'create token success'}))
                else:
                    self.write(json.dumps({'errmsg': u'bad request'}))

                