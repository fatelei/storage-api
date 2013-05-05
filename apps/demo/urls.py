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
from demo.views.file import DemoFileRenameHandler
from demo.views.file import DemoFileExistHandler
from demo.views.file import DemoFilesRemoveHandler
from demo.views.file import DemoFilesDownloadHandler
from demo.views.file import DemoGetUserSpaceHandler

handlers = [
	url("/", DemoLoginHandler, name = 'login'),
	url("/demo/logout", DemoLogoutHandler, name = 'logout'),
	url("/demo/register", DemoRegisterHandler, name = 'register'),
	url("/demo/pwdchange", DemoPwdChangeHandler, name = 'pwdchange'),
	url("/demo/index", DemoIndexHandler, name = 'index'),
	url("/demo/files", DemoFilesHandler, name = 'files'),
	url("/demo/files/upload", DemoFileUploadHandler, name = 'upload'),
	url("/demo/files/rename", DemoFileRenameHandler, name = 'rename'),
	url("/demo/files/exists", DemoFileExistHandler, name = 'exists'),
	url("/demo/files/remove", DemoFilesRemoveHandler, name = 'remove'),
	url("/demo/files/download/(.+)", DemoFilesDownloadHandler, name = 'download'),
	url("/demo/user/space", DemoGetUserSpaceHandler, name = 'space')
]