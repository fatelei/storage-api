#!/usr/bin/env python
#-*-coding: utf8-*-

from base import StorageAPIClient

class File(StorageAPIClient):
    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)

    def get_files(self, **params):
        return self.get("member/files", **params)

    def rename_file(self, **params):
        return self.put("member/files/rename", **params)

    def remove_file(self, **params):
        return self.delete("member/files/remove", **params)

    def search_file(self, **params):
        return self.get("member/files/search", **params)