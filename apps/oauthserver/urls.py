#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.web import url
from oauthserver.views.auth import OAuthLoginHandler, OAuthLogoutHandler, OAuthRegisterHandler
from oauthserver.views.token import AuthorizeTokenHandler, AuthorizeTokenAjaxHandler
from oauthserver.views.token import AdminHandler, AdminTokensAjaxHandler

handlers = [
    url('/', OAuthLoginHandler, name='login'),
    url('/logout', OAuthLogoutHandler, name='logout'),
    url('/register', OAuthRegisterHandler, name='register'),
    url('/token', AuthorizeTokenHandler, name='token'),
    url('/tokenajax', AuthorizeTokenAjaxHandler, name='tokenajax'),
    url('/admin', AdminHandler, name = 'admin'),
    url('/adminajax', AdminTokensAjaxHandler, name = 'adminajax')
]