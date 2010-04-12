#!/usr/bin/env python

import sys, os

todoFile = os.environ['PROJECTS'] + "/todo.txt"

def addTask(task):
	todotxt = open(todoFile, 'a')
	todotxt.write(task)
	todotxt.close()

	print 'task added'

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'usage: todo [ new-task-to-be-added. ]'
	addTask(sys.argv[1])
