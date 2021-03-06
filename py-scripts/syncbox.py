#!/usr/bin/env python

import os, os.path, sys
import hashlib
import sqlite3 as sq
from datetime import datetime as dt

class SyncBoxDB:
   def  __init__(self):
	self.cc = sq.connect("/home/chaitanya/.syncbox.db")
	self.cr = self.cc.cursor()
	try:
		self.cr.execute("""select * from items""")
	except:
		self.createDB()
  
   def createDB(self):
        try:
	    self.cr.execute(""" create table items (name text, added text, hashcontent blob, updated integer) """)
	    self.cc.commit()
	    print "the sqlite syncboxdb is succesfully created!"
        except sq.OperationalError:
	    print "the syncboxdb already exists."

   def addItems(self, rootdir):
	for root, dirs, files in os.walk(rootdir):
	    for file in files:
		filep =  os.path.join(root, file)
		f = open(filep, 'r')
		
		m = hashlib.sha256(f.read())
		t = (filep, dt.now(), m.hexdigest(), 0)
		self.cr.execute(""" insert into items values (?, ?, ?, ?) """, t)

		print "1, :", root, m.hexdigest()

	self.cc.commit()
	print "added a new folder to syncbox : ", root

   def viewByItems(self):
	self.cr.execute("""select * from items""")
	for row in self.cr: print row
	self.cr.close()
  
   def viewByName(self, filep):
	self.cr.execute(""" select * from items where name = %s """ % filep)
	for row in self.cr: print row

   def viewByHash(self, hashkey):

	#for resons beyond my comprehension; this just failed to work;
	#thus resorting to cheap and dirty hacks.
	#self.cr.execute(""" SELECT * FROM items WHERE hashcontent='ba79b1028a7980b767946fd0924964ca3ba88a742ce8865dd29332200d9d19f6' """, hashkey)
	hashkey = " SELECT * FROM items WHERE hashcontent='%s' " %  hashkey

	self.cr.execute(hashkey) 
	for row in self.cr: print row

   def updated(self):
	self.cr.execute(""" SELECT * FROM items WHERE updated=1 """)
	for row in self.cr: print row

if __name__ == '__main__':
	sb = SyncBoxDB()

	if len(sys.argv) >= 3 and sys.argv[1] == "add": 
		sb.addItems(sys.argv[2])

	elif len(sys.argv) >= 3 and sys.argv[1] == "viewname":
 		sb.viewByName(sys.argv[2])

	elif len(sys.argv) >= 3 and sys.argv[1] == "viewhash":
 		sb.viewByHash(sys.argv[2])

	elif len(sys.argv) >= 2 and sys.argv[1] == "viewall": 
		sb.viewByItems()

	elif len(sys.argv) >= 2 and sys.argv[1] == "updated": 
		sb.updated()

	else:
		print 'incorrect usage; hey you need to give a command.'
		print 

