#!/usr/bin/env python
#-*-coding: utf8-*-

import os

BASE_DIR = "/".join(os.path.join(os.path.dirname(__file__)).split('/')[:-1])

SERVER = {
    'gzip': True,
    'debug': True,
    'cookie_secret': 'asdgasduhaioe7qehasdyua8hdeasjkdhysadhakjdh8dasd',
    'xsrf_cookies': True,
    'template_path': '%s/%s' % (BASE_DIR, 'templates'),
    'static_path': '%s/%s' % (BASE_DIR, 'static')
}


APPLY_STATUS = {
    0: "<span class='label label-info'>applying</span>",
    1: "<span class='label label-success'>apply success</span>",
    2: "<span class='label label-error'>apply failed</span>"
}