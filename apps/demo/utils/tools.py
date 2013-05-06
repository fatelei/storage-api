#!/usr/bin/env python
#-*-coding: utf8-*-

import functools
import json

from demo.settings import CORRECT_HTTP_CODE


def render(tpl):
    def decorate(func):
        def Wraps(self, *args, **kwargs):
            status, content = func(self, *args, **kwargs)
            content = json.loads(content)
            err = {'errmsg': ''}
            if int(status['status']) not in CORRECT_HTTP_CODE:
                if not tpl:
                    err['errmsg'] = content['error']['message']
                    self.write(json.dumps(err))
                else:
                    return self.render(tpl, err = err)
            else:
                if not tpl:
                    self.write(json.dumps(content))
                else:
                    return self.render(tpl, user = content)
        return Wraps
    return decorate


def check_status(status):
    if status not in CORRECT_HTTP_CODE:
        return False
    else:
        return True

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