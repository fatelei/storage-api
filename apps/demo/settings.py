#!/usr/bin/env python
#-*-coding: utf8-*-

import os

API_DOMAIN = "https://api.storage.com"
CLIENT_SECRET = '350ae45817264918b561ad352df221e4'
CLIENT_KEY = '0002ad0f13924bd3af5f1eadcd5fdfc2'

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