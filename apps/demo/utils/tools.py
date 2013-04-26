#!/usr/bin/env python
#-*-coding: utf8-*-

from demo.settings import CORRECT_HTTP_CODE

def check_status(status):
	if status not in CORRECT_HTTP_CODE:
		return False
	else:
		return True