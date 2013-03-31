#!/usr/bin/env python
#-*-coding: utf8-*-

import tornado.ioloop

from app import Application
from urls import handlers
from config.settings import SERVER

def run():
    app = Application(handlers, **SERVER)
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()