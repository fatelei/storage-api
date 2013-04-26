#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.web import url

from demo.views.user import DemoLoginHandler
from demo.views.user import DemoLogoutHandler
from demo.views.user import DemoPwdChangeHandler
from demo.views.user import DemoRegisterHandler

handlers = [
	url("/", DemoLoginHandler, name = 'login'),
	url("/demo/logout", DemoLogoutHandler, name = 'logout'),
	url("/demo/register", DemoRegisterHandler, name = 'register'),
	url("/demo/pwdchange", DemoPwdChangeHandler, name = 'pwdchange')
]