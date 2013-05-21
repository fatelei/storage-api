#!/usr/bin/env python
#-*-coding: utf8-*-

from api.controller.member import MemberPwdChange
from api.controller.member import OAuthApiLoginHandler
from api.controller.member import OAuthApiLogoutHandler
from api.controller.member import RegisterHandler
from api.controller.member import MemberInfoHandler
from api.controller.member import MemberSearchHandler
from api.controller.store import FilesHandler
from api.controller.store import FileDownloadHandler
from api.controller.store import FileRemoveHandler
from api.controller.store import FileUpdateHandler
from api.controller.store import FileUploadHandler
from api.controller.store import FileSearchHandler
from api.controller.store import FileIsExistsHandler
from api.controller.store import FilesUsageHandler
from api.controller.store import FileShareDownload
from api.controller.store import FileShareHandler
from api.controller.store import FilesShareListHandler

handlers = [
    ('/member/pwdchange', MemberPwdChange),
    ('/member/search', MemberSearchHandler),
    ('/member/info', MemberInfoHandler),
    ('/member/files', FilesHandler),
    ('/member/files/upload', FileUploadHandler),
    ('/member/files/download', FileDownloadHandler),
    ('/member/files/rename', FileUpdateHandler),
    ('/member/files/remove', FileRemoveHandler),
    ('/member/files/search', FileSearchHandler),
    ('/member/login', OAuthApiLoginHandler),
    ('/member/logout/(\w+)', OAuthApiLogoutHandler),
    ('/member/register', RegisterHandler),
    ('/member/files/search/(\w+)', FileSearchHandler),
    ('/member/files/exists', FileIsExistsHandler),
    ('/member/space', FilesUsageHandler),
    ('/member/file/share', FileShareHandler),
    ('/member/share/fileslist', FilesShareListHandler),
    ('/member/share/file/download', FileShareDownload)
]