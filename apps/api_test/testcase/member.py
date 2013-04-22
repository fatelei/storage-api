#!/usr/bin/env python
#-*-coding: utf8-*-

import unittest

from core.member import Member


class TestMember(unittest.TestCase):
	def setUp(self):
		self.email = "1443343615@qq.com"
		self.password = "123456"

	def test_login(self):
		pass

	def test_pwd_change(self):
		pass

if __name__ == '__main__':
	testsuite = unittest.TestLoader().loadTestsFromTestCase(TestMember)
	unittest.TextTestRunner(verbosity = 2).run(testsuite)