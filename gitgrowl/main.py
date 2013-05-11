#!/usr/bin/python

import sys

usage = 'Usage: '

def run_events():
	pass

def run_stats():
	pass

def run_command(command):
	return {
		'events': run_events(),
		'stats' : run_stats(),
	}.get(command, usage)

def main():
	if len(sys.argv) == 1:
		print usage
	else:
		run_command(sys.argv[1])
