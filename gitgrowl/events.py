#!/usr/bin/python

import os
import ast
import sqlite3
import subprocess
from gitgrowl import default_config

conn = None
config = None

def setup_env():
	config = default_config.config

	with open('.gitgrowl_config', 'w+') as config_file:
		config_file.write(''.join((repr(config))))

	db_file = config['db_file']
	conn = sqlite3.connect(db_file)

	with open('.gitignore', 'a+') as gitignore:
		gitignore.write('\n# gitgrowl\n')
		gitignore.write(''.join(('.gitgrowl_config\n', db_file, '\n')))

def check_db():
	if not os.path.isfile(''.join((os.getcwd(), '/.gitgrowl_config'))):
		setup_env()
	else:
		config = ast.literal_eval(open('.gitgrowl_config', 'r').read())
		conn = sqlite3.connect(config['db_file'])

def get_repo():
	output = subprocess.check_output(["git", "remote", "-v"])
	return output.split()[1][:-4].split('/', 3)[3] 

def check_events():
	check_db()
	repo = get_repo()
	

def events_main(args):
	if len(args) == 1:
		check_events()
