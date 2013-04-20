#!/usr/bin/env python
#-*-coding: utf8-*-

from mongoengine import Q

from api.allin import exceptions
from api.allin.macro import STORAGE_CODE
from api.models.data import File, Files


def check_file_exists(member_id, filename):
    info = {}
    f = File.objects(Q(member_id = member_id) & Q(filename = filename) & Q(is_delete = 0)).first()
    if not f:
        info['code'] = STORAGE_CODE.FILE_NOT_EXISTS
        info['exists'] = False
    else:
        info['code'] = STORAGE_CODE.FILE_IS_EXISTS
        info['exists'] = True
    return info 

def get_files(member_id, offset, limit):
    info = []
    member_files = Files.objects(member_id = member_id).first()
    if not member_files:
        return info
    else:
        files = member_files.files[offset: offset+limit: 1]
        for f in files:
            if not f.is_delete:
                info.append({'filename': f.filename, 'type': f.data.content_type, 'time': f.update_time})
        return info

def download_file(member_id, filename):
    files = Files.objects(member_id = member_id).first()
    info = {}
    if not files:
        info['code'] = STORAGE_CODE.MEMBER_NO_FILES
        info['msg'] = u'no current member'
    elif len(files.files) == 0:
        info['code'] = STORAGE_CODE.FILES_IS_EMPTY
        info['msg'] = u'member has no files'
    else:
        f = File.objects(Q(member_id = member_id) & Q(filename = filename) & Q(is_delete = 0)).first()
        if not f:
            info['code'] = STORAGE_CODE.NOT_EXISTS
            info['msg'] = u'file is not exists'
        elif f in files.files:
            info['code'] = STORAGE_CODE.FILE_GET_OK
            info['data'] = f.data.read()
            info['content_type'] = f.data.content_type
        else:
            info['code'] = STORAGE_CODE.FILE_NOT_BELONG
            info['msg'] = u'file not belong to you'
    return info


def upload_new_file(member_id, filename, data):
    f = File.objects(Q(member_id = member_id))


def update_file_content(member_id, filename):
    pass

def remove_file(member_id, filename):
    files = Files.objects(member_id = member_id).first()
    info = {}
    if not files:
        info['code'] = STORAGE_CODE.MEMBER_NO_FILES
        info['msg'] = u'no current member'
    elif len(files.files) == 0:
        info['code'] = STORAGE_CODE.FILES_IS_EMPTY
        info['msg'] = u'member has no files'
    else:
        f = File.objects(Q(member_id = member_id) & Q(filename = filename) & Q(is_delete = 0)).first()
        if not f:
            info['code'] = STORAGE_CODE.FILE_IS_DELETE
            info['msg'] = u'file has already been deleted' 
        elif f in files.files:
            files.files.remove(f)
            files.save()
            f.is_delete = 1
            f.save()
            info['code'] = STORAGE_CODE.FILE_IS_DELETE
            info['msg'] = u'file is deleted successfully'
        else:
            info['code'] = STORAGE_CODE.FILE_NOT_BELONG
            info['msg'] = 'this file is not yours'
        return info

def modify_file(member_id, filename, *kwargs):
    
