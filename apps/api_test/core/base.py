#!/usr/bin/env python
#-*-coding: utf8-*-

import urllib
import requests

from utils import urlencode, loads

class StorageOAuthClient(object):
    def __init__(self, oauth_url = '', email = '', password = '', client_secret = '', client_key = ''):
        self.oauth_url = oauth_url
        self.email = email
        self.password = password
        self.client_secret = client_secret
        self.client_key = client_key
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

    def basic_login(self):
        body = urllib.urlencode({"grant_type": "password", "email": self.email,
                                 "password": self.password, "client_secret": self.client_secret,
                                 "client_key": self.client_key})
        response = requests.post(self.oauth_url, data = body, headers = self.headers, verify = False)
        status = {}
        status['status'] = response.status_code
        content = response.text
        content = loads(content)
        return status, content

    def basic_logout(self, logout_url):
        response = requests.post(logout_url, data = None, headers = self.headers, verify = False)
        status = {}
        status['status'] = response.status_code
        content = response.text
        content = loads(content)
        return status, content

class StorageAPIClient(object):
    def __init__(self, api_url = '', token = None):
        self.api_url = api_url
        self.token = token
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }

    def execute_request(self, path, method = 'GET', **params):
        params = urlencode(params)
        if method in ['GET', 'DELETE']:
            req_url = "?".join([path, params])
            body = None
        else:
            req_url = path
            body = params.encode("utf8")
        req_url = "/".join([self.api_url, req_url])
        if self.token:
            self.headers['Authorization'] = "bearer:%s" % self.token
        func = getattr(requests, method.lower())
        response = func(req_url, data = body, headers = self.headers, verify = False)
        status = {}
        status['status'] = response.status_code
        content = response.text
        data = loads(content)
        return status, data

    def get(self, path, **params):
        return self.execute_request(path, "GET", **params)

    def post(self, path, **params):
        return self.execute_request(path, "POST", **params)

    def delete(self, path, **params):
        return self.execute_request(path, "DELETE", **params)

    def put(self, path, **params):
        return self.execute_request(path, "PUT", **params)

