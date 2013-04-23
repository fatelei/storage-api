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

    def test_get_files(self):
        offset = 0
        resp, content = self.file.get_files(offset = offset)
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_download_files(self):
        filename = "test.txt"
        resp, content = self.file.download_file(filename = filename)
        self.assertEqual(int(resp['status']), 200)

    def test_upload_files(self):
        register_openers()
        datagen, headers = multipart_encode({"data": open("test.txt", "rb"), "filename": "test.txt", "content_type": "text/plain"})
        headers["Authorization"] = "bearer:%s" % self.token
        request = urllib2.Request("%s/member/files/upload" % config.API_URL, datagen, headers)
        try:
            response = urllib2.urlopen(request)
            code = response.getcode()
            content = response.read()
        except urllib2.HTTPError, e:
            code = e.code
            content = e.msg
        print code
        print content
        self.assertEqual(code, 200)

    @unittest.skip("skip")
    def test_rename_file(self):
        filename = 'test.txt'
        new_filename = 'new_test.txt'
        resp, content = self.file.rename_file(filename = filename, new_filename = new_filename)
        print resp
        self.assertEqual(int(resp['status']), 201)

    @unittest.skip("skip")
    def test_remove_file(self):
        filename = 'test.txt'
        resp, content = self.file.remove_file(filename = filename)
        print resp
        self.assertEqual(int(resp['status']), 200)

    @unittest.skip("skip")
    def test_search_file(self):
        pass

if __name__ == "__main__":
    testsuite = unittest.TestLoader().loadTestsFromTestCase(TestFile)
    unittest.TextTestRunner(verbosity = 2).run(testsuite)