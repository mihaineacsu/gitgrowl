#!/usr/bin/python

import sys
import os
from gitgrowl import events
from gitgrowl import stats

usage = 'Usage: '

def run_command(command):
	return {
		'events': events.events_main(sys.argv[1:]),
		'stats' : stats.stats_main(),
	}.get(command, usage)

def main():
	if len(sys.argv) == 1:
		print usage
	else:
		if not os.path.isdir(''.join((os.getcwd(), '/.git'))):
			print "fatal: Not a git repository"
			return
		if run_command(sys.argv[1]) != None:
			print usage
