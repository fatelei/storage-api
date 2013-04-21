#!/usr/bin/env python
#-*-coding: utf8-*-

from api.controller.base import BaseHandler
from api.allin.macro import MACRO
from api.mixins.store import FileMixin
from api.allin import exceptions

class FilesHandler(BaseHandler, FileMixin):
    def real_get(self):
        offset = int(self.get_argument('offset', MACRO.ZERO))
        return self.api_get_files_list(self.login_id, offset)

class FileDownloadHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        info = {}
        filename = self.get_argument("filename", None)
        if filename:
            info = self.api_download_file(self.login_id, filename)
            return info
        else:
            raise exceptions.ParamsException

class FileUploadHandler(BaseHandler, FileMixin):
    def real_post(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        data = self.get_argument("data", None)
        content_type = self.get_argument("content_type", None)
        if not filename:
            raise exceptions.ParamsException(u"filename is invalid")
        if not data:
            raise exceptions.ParamsException(u"no data upload")
        if not content_type:
            raise exceptions.ParamsException(u"no content type")
        info = self.api_upload_new_files(self.st_member_id)

class FileRemoveHandler(BaseHandler, FileMixin):
    def real_delate(self, *args, **kwargs):
        pass

class FileUpdateHandler(BaseHandler, FileMixin):
    def real_put(self, *args, **kwargs):
        pass

