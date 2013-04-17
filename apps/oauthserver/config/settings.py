#!/usr/bin/env python
#-*-coding: utf8-*-

import os

from tornado.options import define

MONGODB = {
    'host': 'localhost',
    'port': 29701,
    'db': 'storage'
}

BASE_DIR = "/".join(os.path.join(os.path.dirname(__file__)).split('/')[:-1])

SERVER = {
    'gzip': True,
    'debug': True,
    'cookie_secret': 'asdgasduhaioe7qehasdyua8hdeasjkdhysadhakjdh8dasd',
    'xsrf_cookies': True,
    'template_path': '%s/%s' % (BASE_DIR, 'templates'),
    'static_path': '%s/%s' % (BASE_DIR, 'static')
}

define('db', default=MONGODB['db'], help="mongodb name")
define('host', default=MONGODB['host'], help="mongodb host")
define('port', default=MONGODB['port'], help="mongodb port")

