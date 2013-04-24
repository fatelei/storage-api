#!/usr/bin/env python
#-*-coding: utf8-*-

import os

DEBUG = True
SECRET_KEY = "asdafaiohju890uipo4j32423"

base_dir = os.path.realpath(os.path.dirname(__file__))
static_folder = "%s/static" % base_dir
template_folder = "%s/templates" % base_dir
static_url_path = "/static"