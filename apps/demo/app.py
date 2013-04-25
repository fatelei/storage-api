#!/usr/bin/env python
#-*-coding: utf8-*-

import tornado.ioloop

from tornado.options import options
from tornado.web import Application

from demp.urls import handlers
from demo.settings import SERVER

def run():
    options.parse_command_line()
    app = Application(handlers, **SERVER)
    app.listen(1314)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()