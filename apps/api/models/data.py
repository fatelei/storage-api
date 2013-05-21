#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

from datetime import datetime
from mongoengine import Document, FileField, ListField, StringField, EmbeddedDocument,\
                        EmbeddedDocumentField, IntField
from mongoengine import signals

from api.allin.macro import POST_SAVE_LOG_TEMPLATE, PRE_SAVE_LOG_TEMPLATE


class FileShare(Document):
    member_id = StringField(max_length = 40, required = True)
    share_filename = StringField(max_length = 40, required = True)
    share_to_members = ListField(StringField(max_length = 40))
    is_delete = IntField(default = 0)

    meta = {
        'collection': 'share',
        'shard_key': ('member_id',),
        'indexes': ['share_to_members', 'member_id', 'is_delete'],
        'allow_inheritance': False
    }


class File(EmbeddedDocument):
    member_id = StringField(max_length = 40, required = True)
    filename = StringField(max_length = 40, required = True)
    data = FileField()
    is_public = IntField(default = 0)
    is_delete = IntField(default = 0)
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
    member_id = StringField(max_length = 40, required = True, unique = True)
    capacity = IntField(default = 5242880)
    usage = IntField(default = 0)
    files = ListField(EmbeddedDocumentField(File), default = list)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        logging.info(POST_SAVE_LOG_TEMPLATE.format("save", document.member_id, document.capacity))

    meta = {
        'collection': 'member_files',
        'shard_key': ('member_id',),
        'indexes': ['member_id', 'capacity', 'files'],
        'allow_inheritance': False
    }


signals.pre_save.connect(Files.post_save, sender = Files)