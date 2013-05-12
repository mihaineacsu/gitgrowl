#!/usr/bin/python

import os
import ast
import sqlite3
import subprocess
import requests
import getpass
from gitgrowl import setup_env

conn = None
config = None
username = None
password = None

def check_db():
	global config, conn

	if not os.path.isfile(''.join((os.getcwd(), '/.gitgrowl_config'))):
		(config, conn) = setup_env.setup()
	else:
		config = ast.literal_eval(open('.gitgrowl_config', 'r').read())
		conn = sqlite3.connect(config['db_file'])

def get_repourl():
	output = subprocess.check_output(["git", "remote", "-v"])
	repo = output.split()[1][:-4].split('/', 3)[3]
	return ''.join(('https://api.github.com/repos/', repo, '/'))

def get_issues(repo):
	global username, password

	issues_url = ''.join((repo, 'issues'))
	issues = requests.get(issues_url)

	# TODO: add sanity checks for error codes
	if 200 <= issues.status_code < 300:
		return issues
	
	print "Private repo, auth required"
	username = raw_input("Username: ")
	password = getpass.getpass()

	return requests.get(issues_url, auth=(username, password))

def get_pullreq(repo):
	global username, password

	pullreq_url = ''.join((repo, 'pulls'))
	if username != None:
		return requests.get(pullreq_url, auth=(username, password))
	else:
		return requests.get(pullreq_url)

def check_events():
	check_db()
	url = get_repourl()
	issues = get_issues(url)
	pullreq = get_pullreq(url)

def events_main(args):
	if len(args) == 1:
		check_events()
