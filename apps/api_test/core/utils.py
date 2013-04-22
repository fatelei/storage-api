#!/usr/bin/env python
#-*-coding: utf8-*-

import httplib2
import json

from urlparse import urlparse

def format_url(url):
    """
    去掉参数，并格式化 URL
    """
    url = url.split('?')[0]
    if not url.startswith('http://'):
        url = 'http://' + url
    url = urlparse(url)
    return url


def utf8_param(v):
    """
    将参数中的 unicode 及 int 转为 utf8 的 str
    """
    return v.encode('utf-8') if isinstance(v, unicode) else str(v)


def urlencode(params):
    """
    自定义 urlencode，仅做字符串拼接
    """
    if hasattr(params, "items"):
        # mapping objects
        params = params.items()
    else:
        # tuple list
        pass
    l = []
    for k, v in params:
        l.append(k + '=' + utf8_param(v))
    param = '&'.join(l)
    return param.decode('utf-8')
    
def loads(content):
    try:
        data = ujson.loads(content)
    except Exception:
        data = {'error': u'数据返回格式错误'}
    return data


def request(url, method, body, headers):
    http = httplib2.Http()
    resp, content = http.request(url, method=method, body=body, headers=headers)
    return resp, content