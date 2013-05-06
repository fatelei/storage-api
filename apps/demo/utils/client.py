#!/usr/bin/env python
#-*-coding: utf8-*-

import requests
import urllib
import logging

from demo import settings
from demo.utils.tools import urlencode

class APIClient(object):
    def __init__(self):
        self.client_key = settings.CLIENT_KEY
        self.client_secret = settings.CLIENT_SECRET
        self.api_url = settings.API_DOMAIN
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def generate_response(self, response):
        status = {'status': ''}
        status['status'] = response.status_code
        content = response.text
        return status, content

    def oauth_login(self, **params):
        params.update({"grant_type": "password", "client_key": self.client_key,
                       "client_secret": self.client_secret})
        req_url = "%s/member/login" % self.api_url
        response = requests.post(req_url, data = params, headers = self.headers, verify = False)
        return self.generate_response(response)

    def oauth_register(self, **params):
        self.headers['Authorization'] = "oauth:%s" % self.client_key
        req_url = "%s/member/register" % self.api_url
        response = requests.post(req_url, data = params, headers = self.headers, verify = False)
        return self.generate_response(response)

    def oauth_logout(self, **params):
        req_url = "%s/member/logout/%s" % (self.api_url, params['access_token'])
        response = requests.post(req_url, headers = self.headers, verify = False)
        return self.generate_response(response)

    def execute_request(self, path, access_token, method = 'GET', **params):
        if method in ['GET', 'DELETE']:
            params = urlencode(params)
            req_url = "?".join([path, params])
            body = None
        else:
            req_url = path
            body = params
        self.headers['Authorization'] = "bearer:%s" % access_token
        path = "%s/%s" % (self.api_url, req_url)
        func = getattr(requests, method.lower())
        response = func(path, data = body, headers = self.headers, verify = False)
        return self.generate_response(response)

    def upload_file(self, uri, access_token, header, body):
        self.headers['Content-Type'] = header
        self.headers['Authorization'] = "bearer:%s" % access_token
        path = "%s/%s" % (self.api_url, uri)
        response = requests.post(path, data = body, headers = self.headers, verify = False)
        return self.generate_response(response)

    def api_get(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'GET', **params)

    def api_post(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'POST', **params)

    def api_put(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'PUT', **params)

    def api_delete(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'DELETE', **params)