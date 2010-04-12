#!/usr/bin/python

import sys, os, os.path
import simplejson as json
from urllib import urlopen

"""
sample json response from domai.nr

{
    "query": "domai.nr",
    "results": [{
        "domain": "domai.nr",
        "register_url": "http://domai.nr/domai.nr/register",
        "host": "",
        "path": "",
        "subdomain": "domai.nr",
        "availability": "taken"
    }]
}

"""
def finddomain(name):
	url = "%s%s" % ("http://domai.nr/api/json/search?q=", name)
	try:
		httpdata = urlopen(url).read()
	except IOError:
		print "Failed to connect to the network; maybe it's down."
		sys.exit(-2)

	jsondata = json.loads(httpdata)
	print
	print "fetching the results from http://domai.nr"
	print "you queried for : %s" % (jsondata['query']), 
	print " '%d' results found " % (len(jsondata['results']))
	print
	for result in jsondata['results']:
		print "%-15s : %s%s" % (result['availability'], result['domain'], result['path']) 

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "usage ./domainr.py <domain-name1> <domain2> ...."
	
	sys.argv = sys.argv[1:]	
	for arg in sys.argv:
		finddomain(arg)

