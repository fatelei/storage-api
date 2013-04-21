#!/usr/bin/env python
#-*-coding: utf8-*-

import exceptions
import time
import logging

from oauthserver.models.member import Member
from oauthserver.models.token import AccessToken, OAuthToken

class TokenGenerator(object):
    def __init__(self, request):
        self.grant_type = request.get_argument('grant_type', None)
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

    def _validate_client_secret(self, client_secret):
        if not self.member_id:
            raise exceptions.InvalidRequest('email or password is not correct')
        token = OAuthToken.objects(member_id = self.member_id).first()
        if not token:
            raise exceptions.InvalidRequest("you don't have authorize")
        if token.expire < int(time.time()):
            raise exceptions.InvalidRequest("you client secret has expired!")
        if token.client_secret != self.client_secret:
            raise exceptions.InvalidRequest('token is wrong')

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
        access_token = AccessToken()
        access_token.set_access_token()
        access_token.set_refresh_token()
        access_token.set_expire_time()
        access_token.member_id = self.member_id
        access_token.save()
        return access_token