#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import logging
import os

from tornado import web
from demo.views.base import BaseHandler
from demo.utils.tools import render, check_status

class DemoIndexHandler(BaseHandler):
    @render("index.html")
    @web.authenticated
    def get(self):
        token = self.get_secure_cookie("access_token")
        response = self.client.api_get("member/info", token)
        return response


class DemoFilesHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def get(self):
        offset = int(self.get_argument('offset', 1))
        token = self.get_secure_cookie("access_token")
        params = {'offset': offset}
        response = self.client.api_get("member/files", token, **params)
        return response

class DemoFilesDownloadHandler(BaseHandler):
    @web.authenticated
    def get(self, filenames):
        token = self.get_secure_cookie("access_token")
        params = {'filenames': filenames}
        resp, content = self.client.api_get("member/files/download", token, **params)
        content = json.loads(content)
        if check_status(int(resp['status'])):
            if len(content) == 1:
                self.set_header("Content-Type", content[0]['content_type'])
                self.set_header('Content-Disposition', 'attachment; filename='+content[0]['filename'])
                self.write(content[0]['data'])
            else:
                pass
        else:
            self.write(content['error']['message'])

class DemoFileUploadHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def post(self):
        token = self.get_secure_cookie("access_token")
        body = self.request.body
        header = self.request.headers['Content-Type']
        response = self.client.upload_file("member/files/upload", token, header, body)
        return response

class DemoFilesRemoveHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def post(self):
        filenames = self.get_argument("filenames", None)
        if not filenames:
            return {'errmsg': u'no filename'}
        token = self.get_secure_cookie("access_token")
        params = {'filenames': filenames}
        response = self.client.api_delete("member/files/remove", token, **params)
        return response

class DemoFileRenameHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def post(self):
        filename = self.get_argument("filename", None)
        if not filename:
            return {'errmsg': u'no origin filename'}
        new_filename = self.get_argument("new_filename", None)
        if not new_filename:
            return {'errmsg': u'no new filename'}
        token = self.get_secure_cookie("access_token")
        params = {'filename': filename, "new_filename": new_filename}
        response = self.client.api_put("member/files/rename", token, **params)
        return response 

class DemoFileExistHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def post(self):
        filename = self.get_argument("new_filename", None)
        if filename:
            token = self.get_secure_cookie("access_token")
            params = {"filename": filename}
            response = self.client.api_get("member/files/exists", token, **params)
            return response
        else:
            return {'errmsg': u'need input filename'}