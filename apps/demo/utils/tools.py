#!/usr/bin/env python
#-*-coding: utf8-*-

import functools
import json

from demo.settings import CORRECT_HTTP_CODE


def render(func):
    @functools.wraps(func)
    def Wraps(self, *args, **kwargs):
        status, content = func(self, *args, **kwargs)
        err = {'msg': ''}
        if status not in CORRECT_HTTP_CODE:
            err['msg'] = content['error']['message']
            self.write(json.dumps(err))
        else:
            self.write(content)


def check_status(status):
    if status not in CORRECT_HTTP_CODE:
        return False
    else:
        return True
