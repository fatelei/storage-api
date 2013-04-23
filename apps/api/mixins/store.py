#!/usr/bin/env python
#-*-coding: utf8-*-

from api.dao.data import FileDAO
from api.allin.macro import MACRO

class FileMixin(object):
    def api_get_files_list(self, offset = MACRO.ZERO, limit = MACRO.DEFAULT_MAX_COUNT):
        info = FileDAO.get_files(self.login_id, offset, limit)
        return info

    def api_upload_new_files(self, filename, data, content_type):
        info = FileDAO.update_new_file(self.login_id, filename, data, content_type)
        return info

    def api_rename_file(self, filename, new_filename):
        info = FileDAO.modify_file(self.login_id, filename, new_filename)
        return info

    def api_delete_file(self, filename):
        info = FileDAO.remove_file(self.login_id, filename)
        return info

    def api_download_file(self, filename):
        info = FileDAO.download_file(self.login_id, filename)
        return info

    def api_search_files(self, query):
        pass
    