#!/usr/bin/env python
#-*-coding: utf8-*-

import time
import datetime

def convert_time2days(now, created):
    now = time.gmtime(now)
    created = time.gmtime(created)
    now = datetime.datetime.strptime(time.strftime('%Y-%m-%d', now), '%Y-%m-%d')
    created = datetime.datetime.strptime(time.strftime('%Y-%m-%d', created), '%Y-%m-%d')
    timedelta = created - now
    return timedelta.days