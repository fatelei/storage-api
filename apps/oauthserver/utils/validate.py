#!/usr/bin/env python
#-*-coding: utf8-*-

import exceptions
import time
import logging

from mongoengine import Q

from oauthserver.models.member import Member
from oauthserver.models.token import AccessToken, OAuthClient

class TokenGenerator(object):
    def __init__(self, request):
        self.grant_type = request.get_argument('grant_type', None)
        self.client_key = request.get_argument('client_key', None)
        self.client_secret = request.get_argument('client_secret', None)
        self.email = request.get_argument('email', None)
        self.password = request.get_argument('password', None)
        self.request = request
        self.member_id = None

    def validate(self):
        if not self.grant_type:
            raise exceptions.InvalidRequest('params error: no grant_type')
        if self.grant_type not in ['password']:
            raise exceptions.InvalidRequest('unsupport authorize method')
        self._validate_client_secret()
        self._validate_email_password()

    def _validate_client_secret(self):
        if self.client_key:
            self.client = OAuthClient.objects(Q(client_key = self.client_key) & Q(expire__gt = int(time.time()))).first()
        else:
            raise exceptions.InvalidRequest("missing client key")
        if self.client:
            if self.client.client_secret != self.client_secret:
                raise exceptions.InvalidRequest('client secret is wrong')

    def _validate_email_password(self):
        if not self.email:
            raise exceptions.InvalidRequest('invalid email')
        if not self.password:
            raise exceptions.InvalidRequest('invalid passoword')
        member = Member.objects(email = self.email).first()
        if not member:
            raise exceptions.InvalidRequest('email is not correct')
        if not member.check_password(self.password):
            raise exceptions.InvalidRequest('password is not correct')
        self.member_id = member.member_id

    def grant_response(self):
        grant_response_map = {
            "password": "self._grant_password_token()"
        }
        access_token = eval(grant_response_map[self.grant_type])
        data = {
            'token_type': 'bearer',
            'access_token': access_token.access_token,
            'refresh_token': access_token.refresh_token,
            'expire_in': access_token.expire
        }
        return data

    def _grant_password_token(self):
        access_token = AccessToken.objects(Q(member_id = self.member_id) & Q(is_expired = 0)).first()
        if not access_token:
            new_token = AccessToken()
            new_token.set_access_token()
            new_token.set_refresh_token()
            new_token.set_expire_time()
            new_token.member_id = self.member_id
            new_token.save()
            return new_token
        else:
            raise exceptions.InvalidRequest(u"repeated request")