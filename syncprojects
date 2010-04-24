#!/usr/bin/env python

import os

class ENV:
	def __init__(self):
#		self.hostname = os.system('hostname')
		self.projects = os.environ['PROJECTS']
		self.repos = ['git', 'svn']
		self.syncbox = os.path.join(os.environ['HOME'], '.syncbox')


def fetchRepoList(self):
	pass


def startSync(env):
	print
	print 'starting projects sync.. %s' % (env.projects)
	print
	syncbox = open(env.syncbox, 'w')

	for project in os.listdir( env.projects ):

		projectdir = os.path.join(env.projects, project)
		try:
			isgit = os.listdir(projectdir).index('.git')
			print projectdir
		except:
			pass


if __name__ == '__main__':
	env = ENV()
	startSync(env)
