#!/usr/bin/env python
#-*-coding: utf8-*-

from api.controller.base import BaseHandler
from api.allin.macro import MACRO
from api.mixins.store import FileMixin

class FilesHandler(BaseHandler, FileMixin):
    def real_get(self):
        offset = int(self.get_argument('offset', MACRO.ZERO))
        return self.api_get_files_list(offset)

class FileDownloadHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        if filename:
            

class FileUploadHandler(BaseHandler, FileMixin):
    def real_post(self, *args, **kwargs):
        pass

class FileRemoveHandler(BaseHandler, FileMixin):
    def real_delate(self, *args, **kwargs):
        pass

class FileUpdateHandler(BaseHandler, FileMixin):
    def real_put(self, *args, **kwargs):
        pass

