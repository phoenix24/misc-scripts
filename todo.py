#!/usr/bin/env python
import sys, os

""" 
this a simple script to help me manage my todo's.
the current functionalities include,
--add a new task.

--error checking [ comming ]
--delete task
--update task

--sorted views
--tagging; etc.

"""

todoFile = os.environ['PROJECTS'] + "/todo.txt"

def addTask(task):
	todotxt = open(todoFile, 'a')
	todotxt.write(task + "\n")
	todotxt.close()

	print 'task added'

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'usage: todo [ new-task-to-be-added. ]'
		sys.exit(-1)
	addTask(sys.argv[1])
