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
        filenames = self.get_argument("filenames", None)
        if filenames:
            info = self.api_download_file(filenames)
            return info
        else:
            raise exceptions.ParamsException

class FileUploadHandler(BaseHandler, FileMixin):
    def real_post(self, *args, **kwargs):
        data = self.request.files
        if not data:
            raise exceptions.ParamsException(u"no data upload")
        info = self.api_upload_new_files(data)
        return info

class FileRemoveHandler(BaseHandler, FileMixin):
    def real_delete(self, *args, **kwargs):
        filenames = self.get_argument("filenames", None)
        if not filenames:
            raise exceptions.ParamsException(u"need filename")
        info = self.api_delete_file(filenames)
        return info

class FileUpdateHandler(BaseHandler, FileMixin):
    def real_put(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        if not filename:
            raise exceptions.ParamsException(u"no filename")
        new_filename = self.get_argument("new_filename", None)
        if not new_filename:
            raise exceptions.ParamsException(u"no new filename")
        info = self.api_rename_file(filename, new_filename)
        return info

class FileSearchHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        info = []
        query = self.get_argument("query", None)
        if not query:
            return info
        else:
            info = self.api_search_files(query)
            return info

class FileIsExistsHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        filename = self.get_argument('filename', None)
        if not filename:
            return {'exists': False}
        else:
            return self.api_file_exists(filename)

class FilesUsageHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        return self.api_file_usage()
