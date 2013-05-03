#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import logging
import os

from demo.views.base import BaseHandler
from demo.utils.tools import render, authenticated

class DemoIndexHandler(BaseHandler):
    @render("index.html")
    @authenticated
    def get(self):
        token = self.get_secure_cookie("access_token")
        resp, content = self.client.api_get("member/info", token)
        return resp, content


class DemoFilesHandler(BaseHandler):
    @render(None)
    @authenticated
    def get(self):
        offset = int(self.get_argument('offset', 1))
        token = self.get_secure_cookie("access_token")
        params = {'offset': offset}
        resp, content = self.client.api_get("member/files", token, **params)
        return resp, content

class DemoFilesDownloadHandler(BaseHandler):
    @authenticated
    def get(self):
        pass

class DemoFileUploadHandler(BaseHandler):
    @render(None)
    @authenticated
    def post(self):
        token = self.get_secure_cookie("access_token")
        body = self.request.body
        header = self.request.headers['Content-Type']
        resp, content = self.client.upload_file("member/files/upload", token, header, body)
        return resp, content

class DemoFilesRemoveHandler(BaseHandler):
    @authenticated
    def post(self):
        pass

class DemoFileRenameHandler(BaseHandler):
    @authenticated
    def post(self):
        pass