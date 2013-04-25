#!/usr/bin/env python
#-*-coding: utf8-*-

from tornado.web import RequestHandler

from demo.utils.client import APIClient

class BaseHandler(RequestHandler):
	def prepare(self):
		self.client = APIClient()