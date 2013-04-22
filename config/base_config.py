#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.options import define

MONGODB = {
    'host': 'localhost',
    'port': 29701,
    'db': 'storage'
}


define('db', default=MONGODB['db'], help="mongodb name")
define('host', default=MONGODB['host'], help="mongodb host")
define('port', default=MONGODB['port'], help="mongodb port")
define('api_server_port', default = 9000, help = 'api server port')
define('oauth_server_port', default = 8888, help = 'oauth server port')