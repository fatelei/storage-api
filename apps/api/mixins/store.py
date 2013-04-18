#!/usr/bin/env python
#-*-coding: utf8-*-

from api.models.data import Files
from api.allin.macro import MACRO

class FileMixin(object):
    def get_files_list(self, offset = MACRO.ZERO, limit = MACRO.DEFAULT_MAX_COUNT):
        

    def upload_new_files(self, member_id, data):
        pass

    def rename_file(self, member_id, *args, **kwargs):
        pass

    def delete_file(self, member_id, filename):
        pass

    def update_file_content(self, member_id, data):
        pass
    