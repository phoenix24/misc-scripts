#!/usr/bin/python

import sys, os, os.path
import simplejson as json
from urllib import urlopen

"""
this scripts the commandlinefu's from the site, commandlinefu.com in 
json format and displays them in a neat fashion.

"""
def fetchcommands(command):
	requesturl = "http://www.commandlinefu.com/commands/%s/json" % (command)
	try:
		httpdata = urlopen(requesturl).read()
	except IOError:
		print "Failed to connect to the network, maybe it's down."
		sys.exit(-2)

	jsondata = json.loads(httpdata)

	print
	print "%s results fetched from commandlinefu.com" % (len(jsondata))
	print "-------------------"
	for result in jsondata:
		print "command:  %s" % result['command']
		print "summary:  %s" % result['summary']
		print


if __name__ == '__main__':
	fetchcommands("browse/sort-by-votes")
	

	
