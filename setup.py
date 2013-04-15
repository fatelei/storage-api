#!/usr/bin/env python
#-*-coding: utf8-*-

from setuptools import setup, find_packages

install_requires = ['mongoengine',
                    'tornado']

entry_points = """
	[console_script]
	api=api.app:run
	oauth=oauthserver.app:run
"""

setup(
	name = "storage-api",
	author = 'fatelei@gmail.com',
	version = '0.1',
	install_requires = install_requires,
	entry_points = entry_points,
	packages = find_packages('apps'),
	package_dir = ['': 'apps']
)