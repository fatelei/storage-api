#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.options import define

MONGODB = {
    'host': 'mongodb://localhost:29701/storage',
    'db': 'storage',
    'replicaset': 'storage-replset'
}


define('db', default = MONGODB['db'], help = "mongodb name")
define('host', default = MONGODB['host'], help = "mongodb host")
define('replset', default = MONGODB['replicaset'], help = "replica set name")
define('api_server_port', default = 9000, help = "api server port")
define('oauth_server_port', default = 8888, help = "oauth server port")