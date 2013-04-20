#!/usr/bin/env python
#-*-coding: utf8-*-

class HTTP_CODE:
    """
    HTTP Status Code
    """
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    UNSUPPORT_METHOD = 405
    INTERNAL_SERVER_ERROR = 500

class MACRO:
    """
    macro
    """
    ZERO = 0
    DEFAULT_MAX_COUNT = 20

class STORAGE_CODE:
    """
    error code
    """
    FILE_IS_DELETE = 1
    FILE_IS_EXISTS = 2
    FILE_IS_PRIVATE = 3
    FILES_IS_EMPTY = 4
    FILE_NOT_EXISTS = 5
    MEMBER_NO_FILES = 6
    FILE_NOT_BELONG = 7
    FILE_GET_OK = 8
    FILE_DELETE_OK = 9