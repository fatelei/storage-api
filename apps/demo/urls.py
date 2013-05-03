#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.web import url

from demo.views.user import DemoLoginHandler
from demo.views.user import DemoLogoutHandler
from demo.views.user import DemoPwdChangeHandler
from demo.views.user import DemoRegisterHandler
from demo.views.file import DemoIndexHandler
from demo.views.file import DemoFilesHandler
from demo.views.file import DemoFileUploadHandler

handlers = [
	url("/", DemoLoginHandler, name = 'login'),
	url("/demo/logout", DemoLogoutHandler, name = 'logout'),
	url("/demo/register", DemoRegisterHandler, name = 'register'),
	url("/demo/pwdchange", DemoPwdChangeHandler, name = 'pwdchange'),
	url("/demo/index", DemoIndexHandler, name = 'index'),
	url("/demo/files", DemoFilesHandler, name = 'files'),
	url("/demo/files/upload", DemoFileUploadHandler, name = 'upload')
]