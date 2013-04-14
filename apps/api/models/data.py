#!/usr/bin/env python
#-*-coding: utf8-*-

from mongoengine import Document, FileField, ListField, StringField

class Files(Document):
    member_id = StringField(max_length = 40, required = True)
    capacity = IntField(default = 5242880)
    files = ListField(FileField())

    meta = {
        'collection': 'member_files',
        'shard_key': ('member_id',),
        'indexes': ['member_id', 'capacity', 'files'],
        'allow_inheritance': False
    }
