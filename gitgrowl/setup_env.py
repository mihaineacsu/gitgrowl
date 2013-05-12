import sqlite3
from gitgrowl import default_config

def setup():
	"""
	Creates config and db files if they're not found.
	"""
	config = default_config.config

	with open('.gitgrowl_config', 'w+') as config_file:
		config_file.write(''.join((repr(config))))

	db_file = config['db_file']
	conn = sqlite3.connect(db_file)

	with open('.gitignore', 'a+') as gitignore:
		gitignore.write('\n# gitgrowl\n')
		gitignore.write(''.join(('.gitgrowl_config\n', db_file, '\n')))
	
	return (config, conn)
