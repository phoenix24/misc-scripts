#!/usr/bin/env python

import os, os.path
import git
import pyinotify

wm = pyinotify.WatchManager()
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY

exclude_file = [os.path.join(os.getcwd(), '[^\.*]'), 
		'^/home/chaitanya/Projects/scripts/\.*',
		'^/home/chaitanya/Projects/scripts/\.*\.swp']
exclude_files = pyinotify.ExcludeFilter(exclude_file)

class EventHandler(pyinotify.ProcessEvent):
	def process_IN_CREATE(self, event):
		print "creating %s" % ( event.pathname )
	
	def process_IN_MODIFY(self, event):
		print "modified %s" % ( event.pathname )	

	def process_IN_DELETE(self, event):
		print "deleting %s" % ( event.pathname )


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch(os.getcwd(), mask, rec=True, exclude_filter=exclude_files)
notifier.loop()

