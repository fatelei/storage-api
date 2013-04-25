#!/usr/bin/env python
#-*-coding: utf8-*-

from api.controller.member import MemberPwdChange
from api.controller.member import OAuthApiLoginHandler
from api.controller.member import OAuthApiLogoutHandler
from api.controller.member import RegisterHandler
from api.controller.store import FilesHandler
from api.controller.store import FileDownloadHandler
from api.controller.store import FileRemoveHandler
from api.controller.store import FileUpdateHandler
from api.controller.store import FileUploadHandler
from api.controller.store import FileSearchHandler

handlers = [
	('/member/pwdchange', MemberPwdChange),
	('/member/files', FilesHandler),
	('/member/files/upload', FileUploadHandler),
	('/member/files/download', FileDownloadHandler),
	('/member/files/rename', FileUpdateHandler),
	('/member/files/remove', FileRemoveHandler),
	('/member/files/search', FileSearchHandler),
	('/member/login', OAuthApiLoginHandler),
	('/member/logout/(\w+)', OAuthApiLogoutHandler),
	('/member/register', RegisterHandler),
	('/mmember/files/search/(\w+)', FileSearchHandler)
]