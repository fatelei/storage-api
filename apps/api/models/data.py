#!/usr/bin/env python
#-*-coding: utf8-*-

from datetime import datetime
from mongoengine import Document, FileField, ListField, StringField, EmbeddedDocument,\
                        EmbeddedDocumentField, IntField

from api.allin import exceptions

class File(EmbeddedDocument):
    filename = StringField(max_length = 40, required = True)
    data = FileField()
    is_public = IntField(default = 0)
    update_time = StringField(max_length = 40, required = True)

    def set_time(self):
        self.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    meta = {
        'collection': 'file',
        'shard_key': ('filename',),
        'indexes': ['filename'],
        'allow_inheritance': False
    } 

class Files(Document):
    member_id = StringField(max_length = 40, required = True)
    capacity = IntField(default = 5242880)
    files = ListField(EmbeddedDocumentField(File))

    meta = {
        'collection': 'member_files',
        'shard_key': ('member_id',),
        'indexes': ['member_id', 'capacity', 'files'],
        'allow_inheritance': False
    }


def get_files(member_id, offset, limit):
    info = []
    member_files = Files.objects(member_id = member_id).first()
    if not member_files:
        return info
    else:
        files = member_files.files[offset: offset+limit: 1]
        for f in files:
            info.append({'filename': f.filename, 'type': f.data.content_type, 'time': f.update_time})
        return info

def get_spefic_file(member_id, filename):
    files = Files.objects(member_id = member_id).first()
    if not files:
        pass
    elif len(files.files) == 0:
        pass
    else:
        f = File.objects(filename = filename).first()
        if not f:
            pass
        elif f in files.files:
            pass
        else:
            pass

def update_file_content(member_id):
    pass

def remove_file(member_id, filename):
    files = Files.objects(member_id = member_id).first()
    if not files:
        pass
    elif len(files.files) == 0:
        pass
    else:
        f = File.objects(filename = filename).first()
        if not f:
            pass
        elif f in files.files:
            pass
        else:
            pass

def modify_file(member_id, filename, *args):
    pass    
