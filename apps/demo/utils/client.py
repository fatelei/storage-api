#!/usr/bin/env python
#-*-coding: utf8-*-

import httplib2
import urllib

from demo import api_config

class APIClient(object):
    def __init__(self):
        self.client_key = api_config.CLIENT_KEY
        self.client_secret = api_config.CLIENT_SECRET
        self.api_url = api_config.API_DOMAIN
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.http = httplib2.Http()

    def oauth_login(self, **params):
        params.update({"grant_type": "password", "client_key": self.client_key,
                       "client_secret": self.client_secret})
        post_data = urllib.urlencode(params)
        req_url = "%s/member/login" % self.api_url
        response = self.http.request(req_url, method = "POST", body = body, headers = headers)
        return response

    def oauth_register(self, **params):
        self.headers['Authorization'] = "oauth:%s" % self.client_key
        post_data = urllib.urlencode(params)
        req_url = "%s/member/register" % self.api_url
        response = self.http.request(req_url, method = "POST", body = body, headers = headers)
        return response

    def execute_request(self, path, access_token, method = 'GET', **params):
        params = urllib.urlencode(params)
        if method in ['GET', 'DELETE']:
            req_url = "?".join([path, params])
            body = None
        else:
            req_url = path
            body = params
        self.headers['Authorization'] = "bearer:%s" % access_token
        path = "%s/%s" (self.api_url, req_url)
        response = self.http.request(path, method, body = body, headers = headers)
        return response

    def upload_file(self, access_token, **params):
        pass

    def api_get(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'GET', **params)

    def api_post(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'POST', **params)

    def api_put(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'PUT', **params)

    def api_delete(self, uri, access_token, **params):
        return self.execute_request(uri, access_token, 'DELETE', **params)