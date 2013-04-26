#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import logging
import os

from tornado import web

from demo.views.base import BaseHandler
from demo.utils.tools import check_status

class DemoIndexHandler(BaseHandler):
    @web.authenticate
    def get(self):
        token = self.get_secure_cookie("access_token")
        resp, content = self.client.api_get("/member/info", token)
        content = json.loads(content)
        if check_status(int(resp['status'])):
            self.set_secure_cookie("name", content['name'])
            self.render("index.html", user = content)
        else:
            self.write(content)


class DemoFilesHandler(BaseHandler):
    @web.authenticate
    def get(self):
        pass

class DemoFilesDownloadHandler(BaseHandler):
    @web.authenticate
    def get(self):
        pass

class DemoFileUploadHandler(BaseHandler):
    @web.authenticate
    def post(self):
        pass

class DemoFilesRemoveHandler(BaseHandler):
    @web.authenticate
    def post(self):
        pass

class DemoFileRenameHandler(BaseHandler):
    @web.authenticate
    def post(self):
        pass