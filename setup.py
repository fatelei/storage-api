#!/usr/bin/env python
#-*-coding: utf8-*-

from setuptools import setup, find_packages

install_requires = ['mongoengine',
                    'tornado',
                    'blinker',
                    'redis',
                    'redis_shard',
                    'requests']

entry_points = """
	[console_scripts]
	api=api.manage:run
	oauth=oauthserver.manage:run
	demo=demo.app:run
	create_admin=oauthserver.create_admin:run
"""

setup(
	name = "storage-api",
	author = 'fatelei@gmail.com',
	version = '0.1',
	install_requires = install_requires,
	entry_points = entry_points,
	packages = find_packages('apps'),
	package_dir = {'': 'apps'}
)
