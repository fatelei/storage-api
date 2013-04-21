#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.web import url
from oauthserver.views.auth import OAuthLoginHandler, OAuthLogoutHandler, OAuthRegisterHandler, OAuthForApiHandler
from oauthserver.views.token import AuthorizeTokenHandler, AuthorizeTokenAjaxHandler

handlers = [
    url('/', OAuthLoginHandler, name='login'),
    url('/logout', OAuthLogoutHandler, name='logout'),
    url('/register', OAuthRegisterHandler, name='register'),
    url('/token', AuthorizeTokenHandler, name='token'),
    url('/tokenajax', AuthorizeTokenAjaxHandler, name='tokenajax'),
    ('/api_token', OAuthForApiHandler)
]