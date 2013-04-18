#!/usr/bin/env python
#-*-coding: utf8-*-

from mongoengine import Document, FileField, ListField, StringField, EmbeddedDocument,\
						EmbeddedDocumentField, IntField

class File(EmbeddedDocument):
	filename = StringField(max_length = 40, required = 40)
	data = FileField()
	is_public = IntField(default = 0)

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

