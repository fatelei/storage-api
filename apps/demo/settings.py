#!/usr/bin/env python
#-*-coding: utf8-*-

import os

API_DOMAIN = "https://api.storage.com"
CLIENT_SECRET = '4da0e61b6bf24d608bb976ebbf0e2bad'
CLIENT_KEY = '26a3a73f6d344dde941bb8aec54b77c6'

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