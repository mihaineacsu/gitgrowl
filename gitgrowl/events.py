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

class GitHubObject():
	def __init__(self, event):
		self.event_id = event['id']
		self.html_url = event['html_url']
		self.title = event['title']
		self.author = event['user']['login']

		if event['assignee'] != None:
			self.assignee = event['assignee']['login']
		else:
			self.assignee = None

		if event['milestone'] != None:
			self.milestone = event['milestone']['title']
		else:
			self.milestone = None

		if event['body'] != '':
			self.body = event['body']
		else:
			self.body = ''

class GitIssue(GitHubObject):
	def __init__(self, event):
		GitHubObject.__init__(self, event)
		self.number = event['number']

		self.labels = []
		for label in event['labels']:
			self.labels.append(label['name'])
		
		self.pull_request = event['pull_request']['html_url']

class GitPull(GitHubObject):
	def __init__(self, event):
		GitHubObject.__init__(self, event)

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
	"""
	Looks for config and db files, fetches events,
	updates db, displays event if rules apply
	"""
	check_db()
	url = get_repourl()
	issues = get_issues(url)
	pullreq = get_pullreq(url)

	issue_list = []
	for issue in issues.json():
		issue_list.append(GitIssue(issue))

	pull_list = []
	for pull in pullreq.json():
		pull_list.append(GitPull(pull))

def events_main(args):
	if len(args) == 1:
		check_events()
