#!/usr/bin/env python
#-*-coding: utf8-*-

import functools
import logging
import redis
import json

from hashlib import sha1
from api.config.settings import CACHE
from api.utils.decorator import singleton

@singleton
class Memcache(object):
    def __init__(self):
        self._conn = [redis.Redis(**cfg) for cfg in CACHE]
        self._N = len(self._conn)

    def _pos(self, key):
        return int(sha1(key.encode('utf-8')).hexdigest()[:8], 16) % self._N

    @staticmethod
    def cache_key(func, *args):
        return u":".join([func.__name__] + map(unicode, args))

    def cache(self):
        def wraped(func):
            @functools.wraps(func)
            def fcall(obj, *args):
                key = self.cache_key(func, *args)
                rst = self._conn[self._pos(key)].get(key)
                logging.warning(key)
                if not rst:
                    data = func(obj, *args)
                    self._conn[self._pos(key)].setex(key, json.dumps(data), 3600)
                    return data
                return rst
            return fcall
        return wraped

    def invalidate(self, func, *args):
        key = self.cache_key(func, *args)
        self._conn[self._pos(key)].delete(key)

memcache = Memcache()


