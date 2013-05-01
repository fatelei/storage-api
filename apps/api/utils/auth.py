#!/usr/bin/env python
#-*-coding: utf8-*-

import time
import logging

from mongoengine import Q
from oauthserver.models.token import AccessToken, OAuthClient
from api.allin import exceptions

class Authenticator(object):
    def validate(self):
        if "Authorization" not in self.request.headers:
            raise exceptions.InvalidClient
        auth = self.request.headers['Authorization'].split(':')
        auth_type = auth[0].lower()
        auth_value = "".join(auth[1:]).strip()
        if auth_type == 'bearer':
            client = self._validate_bearer(auth_value)
            info = {'member_id': client.member_id, 'type': 'three_leg'}
        elif auth_type == 'oauth':
            client = self._validate_two_leg(auth_value)
            info = {'type': 'two_leg'}
        else:
            raise exceptions.InvalidRequest
        return info

    def _validate_bearer(self, value):
        token = AccessToken.objects(Q(access_token = value) & Q(is_expired = 0)).first()
        if not token:
            raise exceptions.InvalidRequest
        now = int(time.time())
        if token.expire < now:
            raise exceptions.InvalidRequest
        else:
            return token

    def _validate_two_leg(self, value):
        client = OAuthClient.objects(client_key = value).first()
        if not client:
            raise exceptions.InvalidRequest(u"invalid client")
        return client