#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado import web
from mongoengine import connect
from tornado.options import options

class Application(web.Application):
	def __init__(self, handlers=None, default_host='', transforms=None, wsgi=False, **settings):
		connect(options.db, host=options.host, replicaSet = options.replset)
		super(Application, self).__init__(handlers=handlers,
										  default_host=default_host,
										  transforms=transforms,
										  wsgi=wsgi,
										  **settings)