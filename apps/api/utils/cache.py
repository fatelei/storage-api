#!/usr/bin/env python
#-*-coding: utf8-*-

import functools
import logging
import redis
import json

from redis_shard.shard import RedisShardAPI
from hashlib import sha1
from api.config.settings import CACHE
from api.utils.decorator import singleton

@singleton
class Memcache(object):
    def __init__(self):
        self.shard = RedisShardAPI(CACHE)

    @staticmethod
    def cache_key(func, *args):
        return u":".join([func.__name__] + map(unicode, args))

    def cache(self):
        def wraped(func):
            @functools.wraps(func)
            def fcall(obj, *args):
                key = self.cache_key(func, *args)
                rst = self.shard.get(key)
                logging.warning(key)
                if not rst:
                    data = func(obj, *args)
                    self.shard.set(key, json.dumps(data))
                    self.shard.expire(key, 3600)
                    return data
                return rst
            return fcall
        return wraped

    def invalidate(self, func, *args):
        key = self.cache_key(func, *args)
        self.shard.delete(key)

memcache = Memcache()


