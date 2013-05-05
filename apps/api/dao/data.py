#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

from mongoengine import Q

from api.allin import exceptions
from api.allin.macro import STORAGE_CODE
from api.allin.macro import MACRO
from api.models.data import File, Files
from api.utils.tools import capacity_on_fly
from api.utils.enctype import enctype_data
from api.utils.cache import memcache as mc

class FileDAO:
    @classmethod
    def get_enctype_data(cls, data):
        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes = 1)
        async_result = pool.apply_async(enctype_data, [data])
        rst = async_result.get()
        return rst

    @classmethod
    def get_user_space(cls, member_id):
        info = {}
        f = Files.objects(member_id = member_id).only('capacity').first()
        if f:
            info['capacity'] = f.capacity
            return info
        else:
            raise exceptions.BadRequest(u"no such user")

    @classmethod
    def check_file_exists(cls, member_id, filename):
        info = {}
        f = Files.objects(Q(member_id = member_id) & Q(files__member_id = member_id) &\
                          Q(files__filename = filename)).only("member_id").first()
        if not f:
            info['exists'] = False
        else:
            info['exists'] = True
        return info

    @classmethod
    @mc.cache()
    def get_files(cls, member_id):
        info = {}
        member_files, _ = Files.objects.only("files").get_or_create(member_id = member_id)
        if not member_files:
            return info
        else:
            total = len(member_files.files)
            if not total:
                total = 1
            data = []
            files = member_files.files
            for f in files:
                if not f.is_delete:
                    data.append({'filename': f.filename, 'type': f.data.content_type, 'time': f.update_time})
                else:
                    total -= 1
            info["totalpage"] = total/MACRO.DEFAULT_MAX_COUNT if total%MACRO.DEFAULT_MAX_COUNT == 0 else total/MACRO.DEFAULT_MAX_COUNT + 1
            info["data"] = data
            return info

    @classmethod
    def download_file(cls, member_id, filenames):
        filenames = filenames.split(",")
        files = Files.objects(Q(member_id = member_id) & Q(files__member_id = member_id) &\
                              Q(files__filename__in = filenames)).only("files").first()
        info = {}
        data = []
        if not files:
            raise exceptions.BadRequest(u"current member no files")
        else:
            for f in files.files:
                if f.filename in filenames:
                    if not f.is_delete:
                        info['data'] = cls.get_enctype_data(f.data.read())
                        info['content_type'] = f.data.content_type
                        info['filename'] = f.filename
                        data.append(info)
                    else:
                        raise exceptions.BadRequest(u"file has been deleted")
            return data

    @classmethod
    def upload_new_file(cls, member_id, data):
        info = {}
        files = Files.objects(member_id = member_id).first()
        if files:
            length = lambda x: len(x['body'])
            add = lambda x, y: x + y
            need_space = reduce(add, map(length, data))
            print need_space
            cur_capacity = files.capacity
            if need_space > cur_capacity:
                raise exceptions.BadRequest(u"the space is not enough!")
            for d in data:
                has_file = Files.objects(Q(member_id = member_id) & Q(files__filename__exact = d['filename'])).first()
                if has_file:
                    for f in files.files:
                        if f.filename == d['filename']:
                            old_length = f.data.length
                            f.data.new_file(content_type = d['content_type'])
                            f.data.write(cls.get_enctype_data(d['body']))
                            f.data.close()
                            if old_length > f.data.length:
                                files.capacity = capacity_on_fly(cur_capacity, (old_length - f.data.length), 'incr')
                            else:
                                files.capacity = capacity_on_fly(cur_capacity, (f.data.length - old_length), 'updata')
                            files.save()
                            break
                else:
                    new_file = File()
                    new_file.member_id = member_id
                    new_file.filename = d['filename']
                    new_file.set_time()
                    new_file.data.new_file(content_type = d['content_type'])
                    print d['content_type']
                    new_file.data.write(cls.get_enctype_data(d['body']))
                    new_file.data.close()
                    files.update(add_to_set__files = new_file)
                    files.capacity = capacity_on_fly(cur_capacity, new_file.data.length, 'save')
                    files.save()
                info['code'] = STORAGE_CODE.FILE_CREATE_OK
                info['msg'] = u'file(s) uploaded successfully'
        else:
            info['code'] = STORAGE_CODE.MEMBER_NO_FILES
            info['msg'] = u"member has no files"
        mc.invalidate(cls.get_files, member_id)
        return info


    @classmethod
    def remove_file(cls, member_id, filenames):
        files = Files.objects(member_id = member_id).first()
        info = {}
        index = []
        remove_capacity = 0
        if not files:
            info['code'] = STORAGE_CODE.MEMBER_NO_FILES
            info['msg'] = u'no current member'
        elif len(files.files) == 0:
            info['code'] = STORAGE_CODE.FILES_IS_EMPTY
            info['msg'] = u'member has no files'
        else:
            cur_capacity = files.capacity
            filenames = filenames.split(",")
            for f in files.files:
                if f.filename in filenames:
                    index.append(files.files.index(f))
                    f.is_delete = 1
                    remove_capacity += f.data.length
            if index != None:
                for i in index:
                    files.files.pop(i)
                files.capacity = capacity_on_fly(cur_capacity, remove_capacity, 'delete')
                files.save()
                info['code'] = STORAGE_CODE.FILE_DELETE_OK
                info['msg'] = u'file has already been deleted' 
            else:
                info['code'] = STORAGE_CODE.FILE_NOT_DELETE
                info['msg'] = u'file delete failed'
        mc.invalidate(cls.get_files, member_id)
        return info

    @classmethod
    def modify_file(cls, member_id, filename, new_filename):
        files = Files.objects(member_id = member_id).first()
        info = {}
        if not files:
            info['code'] = STORAGE_CODE.MEMBER_NO_FILES
            info['msg'] = u'member has no files'
        else:
            for f in files.files:
                if f.filename == filename:
                    tmp = f.filename.split(".")
                    tmp[0] = new_filename
                    f.filename = ".".join(tmp)
                    files.save()
                    info['code'] = STORAGE_CODE.FILE_UPDATE_OK
                    info['msg'] = u'rename file successfully'
                    mc.invalidate(cls.get_files, member_id)
                    return info
            info['code'] = STORAGE_CODE.FILE_NOT_EXISTS
            info['msg'] = u'file is not exists'
        mc.invalidate(cls.get_files, member_id)
        return info

    @classmethod
    def search_files(cls, member_id, query):
        data = []
        files = Files.objects(Q(member_id = member_id) & Q(files__filename__icontains = query)).only("files").first()
        if not files:
            return data
        else:
            for f in files.files:
                data.append(f.filename)
            return data