#!/usr/bin/env python
#-*-coding: utf8-*-

from api.controller.base import BaseHandler
from api.allin.macro import MACRO
from api.mixins.store import FileMixin

class FilesHandler(BaseHandler, FileMixin):
    def real_get(self):
        offset = int(self.get_argument('offset', MACRO.ZERO))
        

class FileDownloadHandler(BaseHandler, FileMixin):
    pass

class FileUploadHandler(BaseHandler, FileMixin):
    pass

class FileRemoveHandler(BaseHandler, FileMixin):
    pass

