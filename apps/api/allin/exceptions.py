#!/usr/bin/env python
#-*-coding: utf8-*-

class StorageOauthException(Exception):
    def __init__(self, code = None, message = None):
        self.code = code
        self.message = messae

    def __str__(self):
        return "Exception: code = %d, message = '%s'" % (self.code, self.message)

    @property
    def info(self):
        return {'error': {'code': self.code, 'message': self.message}}

class InvalidRequest(StorageOauthException):
    def __init__(self, message = u'invalid request header or params'):
        super(InvalidRequest, self).__init__(code = 600, message = message)

class InvalidToken(StorageOauthException):
    def __init__(self, message = u'invalid token'):
        super(InvalidToken, self).__init__(code = 601, message = message)

class InvalidClient(StorageOauthException):
    def __init__(self, message = u'invalid client'):
        super(InvalidClient, self).__init__(code = 602, message = message)


class StorageApiException(Exception):
    def __init__(self, code = None, message = None):
        self.code = code
        self.message = message

    def __str__(self):
        return "Exception: code = %d, message = '%s'" % (self.code, self.message)

class BadRequest(StorageApiException):
    def __init__(self, message = u'invalid request'):
        super(BadRequest, self).__init__(code = 400, message = message)

class ParamsException(StorageApiException):
    def __init__(self, message = u'invalid params'):
        super(ParamsException, self).__init__(code = 4001, message = message)

class ForbiddenException(StorageApiException):
    def __init__(self, message = u'forbidden op'):
        super(ForbiddenException, self).__init__(code = 403, message = message)

class NotFoundException(StorageApiException):
    def __init__(self, message = u'not found'):
        super(NotFound, self).__init__(code = 404, message = message)

class MethodNotAllowed(StorageApiException):
    def __init__(self, message = u'not allowed method'):
        super(MethodNotAllowed, self).__init__(code = 405, message = message)

class InternalServerError(StorageApiException):
    def __init__(self, message = u'internal server error'):
        super(InternalServerError, self).__init__(code = 500, message = message)