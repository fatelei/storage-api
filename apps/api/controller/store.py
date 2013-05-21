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
            raise exceptions.ParamsException(u"请选择文件上传")
        info = self.api_upload_new_files(data['files'])
        return info

class FileRemoveHandler(BaseHandler, FileMixin):
    def real_delete(self, *args, **kwargs):
        filenames = self.get_argument("filenames", None)
        if not filenames:
            raise exceptions.ParamsException(u"请选择要删除的文件")
        info = self.api_delete_file(filenames)
        return info

class FileUpdateHandler(BaseHandler, FileMixin):
    def real_put(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        if not filename:
            raise exceptions.ParamsException(u"请选择需要重命名的文件")
        new_filename = self.get_argument("new_filename", None)
        if not new_filename:
            raise exceptions.ParamsException(u"请输入新的文件名")
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

class FileShareHandler(BaseHandler, FileMixin):
    def real_put(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        username = self.get_argument("username", None)
        if not filename:
            raise exceptions.ParamsException(u"请选择需要分享的文件")
        if not username:
            raise exceptions.ParamsException(u"请指定要分享给的用户")
        info = self.api_file_share(filename, username)

class FilesShareListHandler(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        offset = int(self.get_argument("offset", MACRO.ZERO))
        info = self.api_get_share_files(offset)
        return info

class FileShareDownload(BaseHandler, FileMixin):
    def real_get(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        if not filename:
            raise exceptions.ParamsException(u"请选择需要下载的文件")
        info = self.api_download_share_file(filename)
        return info