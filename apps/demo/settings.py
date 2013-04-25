#!/usr/bin/env python
#-*-coding: utf8-*-

import os

API_DOMAIN = "localhost:9000"
CLIENT_SECRET = '0084697bc0104e74ba0a9ad4de632552'
CLIENT_KEY = '1bc16f8d72fa4547aafa233bf0ad7331'

CORRECT_HTTP_CODE = [200, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 305, 306, 307]

BASE_DIR = "/".join(os.path.join(os.path.dirname(__file__)).split('/')[:-1])

SERVER = {
    'gzip': True,
    'debug': True,
    'cookie_secret': 'sdifajfhiahdfjnbjhjsahduasdhjhuiewrbnewjrhwejdh8dasd',
    'xsrf_cookies': True,
    'template_path': '%s/%s' % (BASE_DIR, 'templates'),
    'static_path': '%s/%s' % (BASE_DIR, 'static')
}