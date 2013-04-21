#!/usr/bin/env python
#-*-coding: utf8-*-

import urllib

from utils import urlencode, request, loads

class StorageOAuthClient(object):
    def __init__(self, oauth_url = '', email = '', password = '', client_secret = ''):
        self.oauth_url = oauth_url
        self.email = email
        self.password = password
        self.client_secret = client_secret
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

    def basic_login(self):
        body = urllib.urlencode({"grant_type": "password", "email": email,
                                 "password": password, "client_secret": client_secret})
        resp, content = request(self.oauth_url, method = "POST", body = body, headers = self.headers)
        content = loads(content)
        return resp, content


class StorageAPIClient(object):
    def __init__(self, api_url = '', token = None):
        self.api_url = api_url
        self.token = token
        self.header = {
            "Content-type": "application/x-www-form-urlencoded"
        }

    def execute_request(self, path, method = 'GET', **params):
        params = urlencode(params)
        if method in ['GET', 'DELETE']
            req_url = "?".join(path, params)
            body = None
        else:
            req_url = path
            body = params.encode("utf8")
        req_url = "/".join([self.api_url, req_url])
        if self.token:
            self.header['Authorization'] = "bearer:%s" % self.token
        resp, content = request(req_url, method, body, headers)
        data = loads(content)
        return resp, data

    def get(self, path, **params):
        return self.execute_request(path, "GET", **params)

    def post(self, path, **params):
        return self.execute_request(path, "POST", **params)

    def delete(self, path, **params):
        return self.execute_request(path, "DELETE", **params)

    def put(self, path, **params):
        return self.execute_request(path, "PUT", **params)
