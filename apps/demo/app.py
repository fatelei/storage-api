#!/usr/bin/env python
#-*-coding: utf8-*-

from flask import Flask

from demo import server_config

app = Flask(__name__, static_url_path = server_config.static_url_path, static_folder = server_config.static_folder, template_folder = server_config.template_folder)
app.config.from_object("demo.server_config")