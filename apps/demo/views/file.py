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
        response = self.client.api_get("member/info", token)
        return response


class DemoFilesHandler(BaseHandler):
    @render(None)
    @authenticated
    def get(self):
        offset = int(self.get_argument('offset', 1))
        token = self.get_secure_cookie("access_token")
        params = {'offset': offset}
        response = self.client.api_get("member/files", token, **params)
        return response

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
        response = self.client.upload_file("member/files/upload", token, header, body)
        return response

class DemoFilesRemoveHandler(BaseHandler):
    @authenticated
    def post(self):
        pass

class DemoFileRenameHandler(BaseHandler):
    @render(None)
    @authenticated
    def post(self):
        filename = self.get_argument("filename", None)
        if not filename:
            return {'msg': u'no origin filename'}
        new_filename = self.get_argument("new_filename", None)
        if not new_filename:
            return {'msg': u'no new filename'}
        token = self.get_secure_cookie("access_token")
        params = {'filename': filename, "new_filename": new_filename}
        response = self.client.api_post("member/files/rename", token, **params)
        return response 

class DemoFileExistHandler(BaseHandler):
    @render(None)
    @authenticated
    def post(self):
        filename = self.get_argument("new_filename", None)
        if filename:
            token = self.get_secure_cookie("access_token")
            params = {"filename": filename}
            response = self.client.api_get("member/files/exists", token, **params)
            return response
        else:
            return {'msg': u'need input filename'}