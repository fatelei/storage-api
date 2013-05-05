#!/usr/bin/env python
#-*-coding: utf8-*-

import os

API_DOMAIN = "http://localhost:9000"
CLIENT_SECRET = '8ee018740c164c2e8d72fbda8cdb8a1a'
CLIENT_KEY = 'd74c27251e404364b5da170622c57bce'

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

TMPDIR = "/".join([BASE_DIR, "tmp"])