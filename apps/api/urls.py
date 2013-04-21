#!/usr/bin/env python
#-*-coding: utf8-*-

from api.controller.member import MemberPwdChange
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
	('/member/files/search', FileSearchHandler)
]