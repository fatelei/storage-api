#!/usr/bin/env python
#-*-coding: utf8-*-

import base_config
import tornado.ioloop

from tornado.options import options
from app import Application
from urls import handlers
from api.config.settings import SERVER

application = Application(handlers, **SERVER)

def run():
    options.parse_command_line()
    app = Application(handlers, **SERVER)
    app.listen(options.api_server_port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()