#!/usr/bin/env python
#-*-coding: utf8-*-

from demo.app import app
from flask import request, render_template

@app.route("/demo/login", methods = ['GET', 'POST'])
def oauth_login():
	if request.method == 'POST':
		