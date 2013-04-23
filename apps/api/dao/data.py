#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

from mongoengine import Q

from api.allin import exceptions
from api.allin.macro import STORAGE_CODE
from api.models.data import File, Files

class FileDAO:
    @classmethod
    def check_file_exists(cls, member_id, filename):
        info = {}
        f = Files.objects(Q(member_id = member_id) & Q(files__member_id = member_id) &\
                          Q(files__filename = filename)).only("member_id").first()
        if not f:
            info['code'] = STORAGE_CODE.FILE_NOT_EXISTS
            info['exists'] = False
        else:
            info['code'] = STORAGE_CODE.FILE_IS_EXISTS
            info['exists'] = True
        return info

    @classmethod
    def get_files(cls, member_id, offset, limit):
        info = {}
        member_files, _ = Files.objects.only("files").get_or_create(member_id = member_id)
        if not member_files:
            return info
        else:
            total = len(member_files.files)
            data = []
            files = member_files.files[offset: offset+limit: 1]
            for f in files:
                if not f.is_delete:
                    data.append({'filename': f.filename, 'type': f.data.content_type, 'time': f.update_time})
            info["pages"] = total
            info["now_page"] = offset
            info["data"] = data
            return info

    @classmethod
    def download_file(cls, member_id, filename):
        f = Files.objects(Q(member_id = member_id) & Q(files__member_id = member_id) &\
                          Q(files__filename = filename)).only("files").first()
        info = {}
        if not files:
            info['code'] = STORAGE_CODE.MEMBER_NO_FILES
            info['msg'] = u'no current member'
        elif len(files.files) == 0:
            info['code'] = STORAGE_CODE.FILES_IS_EMPTY
            info['msg'] = u'member has no files'
        else:
            for f in files:
                if f.filename == filename:
                    if not f.is_delete:
                        info['code'] = STORAGE_CODE.FILE_GET_OK()
                        info['data'] = f.data.read()
                        info['content_type'] = f.data.content_type
                    else:
                        info['code'] = STORAGE_CODE.FILE_NOT_EXISTS
                        info['msg'] = u'file is not exists'
                    break
            if 'data' not in info:
                info['code'] = STORAGE_CODE.FILE_NOT_EXISTS
                info['msg'] = u'file is not exists'
        return info

    @classmethod
    def upload_new_file(cls, member_id, filename, data, content_type):
        info = {}
        flag = True
        files = Files.objects(member_id = member_id).first()
        for f in files.files:
            if f.filename == filename:
                flag = False
                f.data.new_file()
                f.data.write(data['data'][0]['body'])
                f.data.content_type = content_type
                f.data.close()
                files.save()
                info['code'] = STORAGE_CODE.FILE_UPDATE_OK
                info['msg'] = u'file has been updated'
                return info
        if flag:
            if len(data) < files.capacity:
                new_file = File()
                new_file.member_id = member_id
                new_file.filename = filename
                new_file.set_time()
                new_file.data.new_file()
                new_file.data.write(data['data'][0]['body'])
                new_file.data.close()
                files.update(push__files = new_file)
                files.reload()
                files.save()
                info['code'] = STORAGE_CODE.FILE_CREATE_OK
                info['msg'] = u'file create successfully'
            else:
                info['code'] = STORAGE_CODE.FILE_NO_SPACE
                info['msg'] = u'no space for upload'
            return info

    @classmethod
    def remove_file(cls, member_id, filename):
        files = Files.objects(member_id = member_id).first()
        info = {}
        index = None
        remove_capacity = 0
        if not files:
            info['code'] = STORAGE_CODE.MEMBER_NO_FILES
            info['msg'] = u'no current member'
        elif len(files.files) == 0:
            info['code'] = STORAGE_CODE.FILES_IS_EMPTY
            info['msg'] = u'member has no files'
        else:
            for f in files.files:
                if f.filename == filename:
                    index = files.files.index(f)
                    f.is_delete = 1
                    remove_capacity = f.data.length
                    break
            if index:
                files.files.pop(index)
                cur_capacity = files.capacity
                files.capacity = cur_capacity + remove_capacity
                files.save()
                info['code'] = STORAGE_CODE.FILE_DELETE_OK
                info['msg'] = u'file has already been deleted' 
            else:
                info['code'] = STORAGE_CODE.FILE_NOT_DELETE
                info['msg'] = u'file delete failed'
            return info

    @classmethod
    def modify_file(cls, member_id, filename, new_filename):
        files = Files.object(member_id = member_id).first()
        info = {}
        if not files:
            info['code'] = STORAGE_CODE.MEMBER_NO_FILES
            info['msg'] = u'member has no files'
        else:
            for f in files.files:
                if f.filename == filename:
                    f.filename = new_filename
                    files.save()
                    info['code'] = STORAGE_CODE.FILE_UPDATE_OK
                    info['msg'] = u'rename file successfully'
                    return info
            info['code'] = STORAGE_CODE.FILE_NOT_EXISTS
            info['msg'] = u'file is not exists'
            return info

    @classmethod
    def search_files(cls, query):
        pass