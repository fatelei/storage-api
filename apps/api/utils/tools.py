#!/usr/bin/env python
#-*-coding: utf8-*-

import logging

def capacity_on_fly(cur_capacity, delta_capacity, action):
    if action in ['save', 'update']:
        cur_capacity = cur_capacity - delta_capacity
    else:
        cur_capacity = cur_capacity + delta_capacity
    return cur_capacity

