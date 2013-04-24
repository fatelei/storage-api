#!/usr/bin/env python
#-*-coding: utf8-*-

import random

from api.config.settings import ENCTYPE_KEY

def enctype_data(data):
    random.seed(ENCTYPE_KEY)
    data = map(ord, data)
    length = len(data)
    rst = []
    for i in range(length):
        rst.append(data[i] ^ random.randint(0, 255))
    return "".join(map(chr, rst))
