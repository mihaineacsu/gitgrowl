from setuptools import setup

with open('./README.md', 'r') as readme_file:
    readme_description = readme_file.read()

setup(
	name='gitgrowl',
	version='0.1',
	author='Mihai Neacsu',
	author_email='mihai.neacsu@ymail.com',
	url='https://github.com/mihaineacsu/gitgrowl',
	packages=['gitgrowl'],
	download_url='https://github.com/mihaineacsu/gitgrowl',
	description='Github repository activity aggregator',
	long_description=readme_description,
	platforms='any',
	install_requires=['requests', 'pysqlite',],
	entry_points={
		'console_scripts': [
			'gitgrowl = gitgrowl.main:main',
			]
		},
)
