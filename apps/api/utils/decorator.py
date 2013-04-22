#!/usr/bin/env python
#-*-coding: utf8-*-

import logging
import functools

from ujson import dumps

from api.allin import exceptions
from api.allin.macro import HTTP_CODE

def ExceptionHandler(f):
    def wrapper(self, *args, **kwargs):
        try:
            info = f(self, *args, **kwargs)
            return self.finish(dumps(info))
        except exceptions.BadRequest, e:
            self.set_status(HTTP_CODE.BAD_REQUEST)
            logging.warning(e)
        except exceptions.ForbiddenException, e:
            self.set_status(HTTP_CODE.FORBIDDEN)
            logging.warning(e)
        except exceptions.NotFoundException, e:
            self.set_status(HTTP_CODE.NOT_FOUND)
            logging.warning(e)
        except exceptions.StorageApiException, e:
            self.set_status(HTTP_CODE.BAD_REQUEST)
            logging.warning(e, exc_info = True)
        except Exception, e:
            self.set_status(HTTP_CODE.INTERNAL_SERVER_ERROR)
            e = exceptions.InternalServerError(e.message)
            logging.warning(e, exc_info = True)
        return self.finish(dumps(e.info))
    return wrapper

def singleton(cls):
    instances = {}
    @functools.wraps(cls, ('__module__', '__name__'), {})
    class _Wraped(cls):
        def __new__(self, *args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
    return _Wraped