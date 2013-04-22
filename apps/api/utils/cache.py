#!/usr/bin/env python
#-*-coding: utf8-*-

import functools

from redis_shard.shard import RedisShardAPI

from api.config.settings import 
from api.utils.decorator import singleton

@singleton
class Memcache(object):
    def __init__(self):
        self.shard = RedisShardAPI(CACHE)

    @staticmethod
    def cache_key(f, *args):
        

    def cache(func, key_func = None):
        def wraped(func):
            @functools.wraps(func)
            def fcall(cls, *args, **kwargs):
                cache_key = fcall.key_func(cls, *args, **kwargs)
                rst = mc.get(cache_key)
                if rst is None:
                    pass
                else:
                    pass
            fcall.nocache = func
            fcall.key_func = key_func or 
            return fcall

