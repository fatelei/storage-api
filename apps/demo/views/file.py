#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import logging
import os

from tornado import web

from demo.views.base import BaseHandler
from demo.utils.tools import check_status

class DemoIndexHandler(BaseHandler):
    @web.authenticated
    def get(self):
        token = self.get_secure_cookie("access_token")
        resp, content = self.client.api_get("member/info", token)
        content = json.loads(content)
        if check_status(int(resp['status'])):
            self.set_secure_cookie("name", content['name'])
            self.render("index.html", user = content)
        else:
            self.write(content)


class DemoFilesHandler(BaseHandler):
    @web.authenticated
    def get(self):
        offset = int(self.get_argument('offset', 1))
        token = self.get_secure_cookie("access_token")
        params = {'offset': offset}
        resp, content = self.client.api_get("member/files", token, **params)
        err = {'msg': ''}
        print content
        if check_status(int(resp['status'])):
            self.write(content)
        else:
            err['msg'] = content['error']['message']
            self.write(json.dumps(err))

class DemoFilesDownloadHandler(BaseHandler):
    @web.authenticated
    def get(self):
        pass

class DemoFileUploadHandler(BaseHandler):
    @web.authenticated
    def post(self):
        print self.request.files

class DemoFilesRemoveHandler(BaseHandler):
    @web.authenticated
    def post(self):
        pass

class DemoFileRenameHandler(BaseHandler):
    @web.authenticated
    def post(self):
        pass