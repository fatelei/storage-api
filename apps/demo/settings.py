#!/usr/bin/env python
#-*-coding: utf8-*-

import os

API_DOMAIN = "http://localhost:9000"
CLIENT_SECRET = '26bd3f79da3347f5b03d853a8f612268'
CLIENT_KEY = '88a024e216b14417b8757370ff9bda26'

CORRECT_HTTP_CODE = [200, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 305, 306, 307]

BASE_DIR = "/".join(os.path.join(os.path.dirname(__file__)).split('/'))

SERVER = {
    'gzip': True,
    'debug': True,
    'cookie_secret': 'sdifajfhiahdfjnbjhjsahduasdhjhuiewrbnewjrhwejdh8dasd',
    'xsrf_cookies': True,
    'template_path': '%s/%s' % (BASE_DIR, 'templates'),
    'static_path': '%s/%s' % (BASE_DIR, 'static')
}