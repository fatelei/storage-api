#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

from api.controller.base import BaseHandler
from api.allin.macro import MACRO
from api.mixins.store import FileMixin
from api.allin import exceptions

class FilesHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        offset = int(self.get_argument('offset', MACRO.ZERO))
        return self.api_get_files_list(offset = offset)

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
        data = self.request.files
        content_type = self.get_argument("content_type", None)
        logging.warning(filename)
        logging.warning(content_type)
        if not filename:
            raise exceptions.ParamsException(u"filename is invalid")
        if not data:
            raise exceptions.ParamsException(u"no data upload")
        if not content_type:
            raise exceptions.ParamsException(u"no content type")
        info = self.api_upload_new_files(filename, data, content_type)
        return info

class FileRemoveHandler(BaseHandler, FileMixin):
    def real_delate(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        if not filename:
            raise exceptions.ParamsException(u"need filename")
        info = self.api_delete_file(self.login_id, filename)
        return info

class FileUpdateHandler(BaseHandler, FileMixin):
    def real_put(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        if not filename:
            raise exceptions.ParamsException(u"no filename")
        new_filename = self.get_argument("new_filename", None)
        if not new_filename:
            raise exceptions.ParamsException(u"no new filename")
        info = self.api_rename_file(self.login_id, filename, new_filename)
        return info

class FileSearchHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        pass

