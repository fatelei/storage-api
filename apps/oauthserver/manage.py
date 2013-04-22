#!/usr/bin/env python
#-*-coding: utf8-*-

import base_config
import tornado.ioloop

from tornado.options import options

from oauthserver.app import Application
from oauthserver.urls import handlers
from oauthserver.config.settings import SERVER

def run():
    options.parse_command_line()
    app = Application(handlers, **SERVER)
    app.listen(options.oauth_server_port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()