#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.options import define

from oauthserver.config.settings import MONGODB

define('db', default = MONGODB['db'], help = 'database name')
define('host', default = MONGODB['host'], help = 'mongodb host')
define('port', default = MONGODB['port'], help = 'mongodb port')

SERVER = {
    'gzip': True,
    'debug': True
}

CACHE = {
	'host': 'localhost',
	'port': 6700,
	'db': 0
}