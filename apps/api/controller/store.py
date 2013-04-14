#!/usr/bin/env python
#-*-coding: utf8-*-

from base import BaseHandler
from api.allin.macro import MACRO
from api.mixins.store import FileMixin

class FilesHandler(BaseHandler, FileMixin):
	def real_get(self):
		offset = int(self.get_argument('offset', MACRO.ZERO))
		