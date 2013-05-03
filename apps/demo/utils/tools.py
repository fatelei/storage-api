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
            err = {'msg': ''}
            if int(status['status']) not in CORRECT_HTTP_CODE:
                if not tpl:
                    err['msg'] = content['error']['message']
                    self.write(json.dumps(err))
                else:
                    return self.render(tpl, err = err)
            else:
                if not tpl:
                    self.write(content)
                else:
                    return self.render(tpl, user = content)
        return Wraps
    return decorate


def authenticated(method):
    """
    hack the tornado authenticated decorator
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


def check_status(status):
    if status not in CORRECT_HTTP_CODE:
        return False
    else:
        return True
