#!/usr/bin/env python
#-*-coding: utf8-*-

import unittest
import urllib2
import config

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from core.file import File

class TestFile(unittest.TestCase):
    def setUp(self):
        self.file = File(api_url = config.API_URL, token = config.TOKEN)
        self.token = config.TOKEN

    @unittest.skip("skip")
    def test_get_files(self):
        offset = 0
        resp, content = self.file.get_files(offset = offset)
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_download_files(self):
        filenames = "test.txt"
        resp, content = self.file.download_file(filenames = filenames)
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_upload_files(self):
        register_openers()
        datagen, headers = multipart_encode({"files": open("test.txt", "rb")})
        headers["Authorization"] = "bearer:%s" % self.token
        request = urllib2.Request("%s/member/files/upload" % config.API_URL, datagen, headers)
        try:
            response = urllib2.urlopen(request)
            code = response.getcode()
            content = response.read()
        except urllib2.HTTPError, e:
            code = e.code
            content = e.msg
        self.assertEqual(code, 200)

    @unittest.skip("skip")
    def test_rename_file(self):
        filename = 'test.txt'
        new_filename = 'new_test.txt'
        resp, content = self.file.rename_file(filename = filename, new_filename = new_filename)
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_remove_file(self):
        filenames = 'new_test.txt'
        resp, content = self.file.remove_file(filenames = filenames)
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_search_file(self):
        query = 'test'
        resp, content = self.file.search_file(query = query)
        self.assertEqual(int(resp['status']), 200)

    
    def test_share_file(self):
        filename = "test.txt"
        username = "testuser"
        resp, content = self.file.share_file(filename = filename, username = username)
        self.assertEqual(int(resp['status']), 200)

if __name__ == "__main__":
    testsuite = unittest.TestLoader().loadTestsFromTestCase(TestFile)
    unittest.TextTestRunner(verbosity = 2).run(testsuite)
