#!/usr/bin/env python
#-*-coding: utf8-*-

import json
import logging
import os

from tornado import web
from demo.views.base import BaseHandler
from demo.utils.tools import render, check_status
from demo.settings import TMPDIR

class DemoIndexHandler(BaseHandler):
    @render("index.html")
    @web.authenticated
    def get(self):
        token = self.get_secure_cookie("access_token")
        response = self.client.api_get("member/info", token)
        _, content = response
        content = json.loads(content)
        self.set_secure_cookie("name", content['name'])
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
                need_rm = []
                username = self.get_secure_cookie("name")
                os.chdir(TMPDIR)
                os.system("mkdir {0}".format(username))
                os.chdir(username)
                for data in content:
                    f = file(data['filename'], "w")
                    f.write(data['data'])
                    f.close()
                os.chdir(TMPDIR)
                download_name = "{0}-download.tar.gz".format(username)
                command = "tar -czf {0} {1}".format(download_name, username)
                os.system(command)
                self.set_header("Content-Type", "application/octet-stream")
                self.set_header("Content-Disposition", 'attachment; filename='+download_name)
                f = file(download_name, "rb")
                data = f.read()
                f.close()
                command = "rm -rf {0} {1}".format(username, download_name)
                os.system(command)
                self.write(data)
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

class DemoGetUserSpaceHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def get(self):
        token = self.get_secure_cookie("access_token")
        response = self.client.api_get("member/space", token)
        return response


class DemoFileShareHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def post(self):
        filename = self.get_argument("filename", None)
        if not filename:
            return {'errmsg': u'请指定要分享的文件'}
        username = self.get_argument("username", None)
        if not username:
            return {'errmsg': u'请指定要分享给的用户'}
        token = self.get_secure_cookie("access_token")
        params = {"filename": filename, "username": username}
        response = self.client.api_put("member/file/share", token, **params)
        return response


class DemoSearchMemberHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def get(self):
        token = self.get_secure_cookie("access_token")
        response = self.client.api_get("member/search", token)
        return response

class DemoFilesListHandler(BaseHandler):
    @render(None)
    @web.authenticated
    def get(self):
        offset = int(self.get_argument("offset", 1))
        token = self.get_secure_cookie("access_token")
        params = {"offset": offset}
        response = self.client.api_get("member/share/fileslist", token, **params)
        return response


class DemoFileShareDownload(BaseHandler):
    @render(None)
    @web.authenticated
    def get(self):
        pass