#!/usr/bin/python

from gitgrowl import os
from gitgrowl import sqlite3
from gitgrowl import default_config

conn = None

def setup_env():
	config = default_config.config

	with open('.gitgrowl_config', 'w+') as config_file:
		config_file.write(''.join(('config=', repr(config))))

	db_file = config['db_file']
	conn = sqlite3.connect(db_file)

	with open('.gitignore', 'a+') as gitignore:
		gitignore.write('\n# gitgrowl\n')
		gitignore.write(''.join(('.gitgrowl_config\n', db_file)))

def check_db():
	if not os.path.isfile(''.join((os.getcwd(), '/.gitgrowl_config'))):
	   setup_env() 

def check_events():
	check_db()

def events_main(args):
	if len(args) == 1:
		check_events()
