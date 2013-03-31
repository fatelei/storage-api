#!/usr/bin/env python
#-*-coding: utf8-*-

class OAuthException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super(OAuthException, self).__init__()

    def __str__(self):
        return "Exception: code=%d, message='%s'" % (self.code, self.message)

    @property
    def info(self):
        return {'error': {'code': self.code, 'message': self.message}}

class InvalidRequest(OAuthException):
    def __init__(self, message=u'请求验证失败，参数不完整、用户名密码错误等！'):
        super(InvalidRequest, self).__init__(code=101, message=message)

