#!/usr/bin/env python
#-*-coding: utf8-*-

import urllib
import httplib2

def api_auth(email, password):
	data = {"email": email, "password": password}
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	body = urllib.urlencode(data)
	http = 

def api_register(data):
	pass

def api_logout(token):
	pass