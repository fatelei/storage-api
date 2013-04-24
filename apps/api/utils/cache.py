#!/usr/bin/env python
#-*-coding: utf8-*-

import functools

from redis_shard.shard import RedisShardAPI

from api.config.settings import CACHE
from api.utils.decorator import singleton

@singleton
class Memcache(object):
    def __init__(self):
        self.shard = RedisShardAPI(CACHE)

    @staticmethod
    def cache_key(func, *args):
        return u":".join([func.__name__] + map(unicode, *args))

    def cache(self, func):
        @functools.wraps(func)
        def Wraped(obj, *args, **kwargs):
            key = self.cache(func, *args)
            rst = self.shard.get(key)
            if not rst:
                data = func(obj, *args, **kwargs)
                self.shard.set(data, 3600)
                return data
            return rst
        return Wraped

    def invalidate(self, func, *args):
        key = self.cache_key(func, *args)
        self.shard.delete(key)


