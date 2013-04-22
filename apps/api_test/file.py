#!/usr/bin/env python
#-*-coding: utf8-*-

import unittest

from core.file import File

class TestFile(unittest.TestCase):
	def setUp(self):
		self.file = File(api_url = '', token = '')

	def test_get_files(self):
		offset = 0
		resp, content = self.file.get_files(offset = offset)
		self.assertEqual(int(resp['status']), 200)

	def test_download_files(self):
		filename = ''
		resp, content = self.file.download_file(filename = filename)
		self.assertEqual(int(resp['status']), 200)

	def test_upload_files(self):
		filename = ''
		content_type = ''
		resp, content = self.file.upload_file(filename = filename, content_type = content_type)
		self.assertEqual(int(resp['status']), 201)

	def test_rename_file(self):
		filename = ''
		new_filename = ''
		resp, content = self.file.rename_file(filename = filename, new_filename = new_filename)
		print resp
		self.assertEqual(int(resp['status']), 201)

	def test_remove_file(self):
		filename = ''
		resp, content = self.file.remove_file(filename = filename)
		print resp
		self.assertEqual(int(resp['status']), 200)

	@unittest.skip
	def test_search_file(self):
		pass

if __name__ == "__main__":
	testsuite = unittest.TestLoader().loadTestsFromTestCase(TestFile)
	unittest.TextTestRunner(verbosity = 2).run(testsuite)