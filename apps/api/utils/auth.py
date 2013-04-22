#!/usr/bin/env python
#-*-coding: utf8-*-

import time
import logging

from oauthserver.models.token import AccessToken
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
            info = {'member_id': client.member_id}
        else:
            raise exceptions.InvalidRequest
        return info

    def _validate_bearer(self, value):
        token = AccessToken.objects(access_token = value).first()
        if not token:
            raise exceptions.InvalidRequest
        now = int(time.time())
        if token.expire < now:
            raise exceptions.InvalidRequest
        else:
            return token