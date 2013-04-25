#!/usr/bin/env python
#-*-coding: utf8-*-

from demo.app import app
from flask import request, render_template

@app.route("/demo/login", methods = ['GET', 'POST'])
def oauth_login():
	if request.method == 'POST':
		pass
	else:
		pass

@app.route("/demo/register", method = ['GET', 'POST'])
def oauth_register():
	if request.method == 'POST':
		pass
	else:
		pass

@app.route("/demo/logout", method = ['GET'])
def oauth_logout():
	pass

@app.route("/demo/pwdchange", method = ['GET', 'POST'])
def change_password():
	pass
		