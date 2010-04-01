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
	httpdata = urlopen(requesturl).read()
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
	

	
