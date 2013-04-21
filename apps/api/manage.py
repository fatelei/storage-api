#!/usr/bin/env python
#-*-coding: utf8-*-

import tornado.ioloop

from tornado.options import options
from app import Application
from urls import handlers
from config.settings import SERVER

def run():
	options.parse_command_line()
    app = Application(handlers, **SERVER)
    app.listen(options.server_port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()