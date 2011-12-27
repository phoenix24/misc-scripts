#!/usr/bin/env python 

import os
import md5

sum = []
duplicate = "./duplicate/"

def search(digest):
	for i in sum:
		if i == digest:
			return False
	return True

def dupname(cnt, fpath, bool=True):
	l = fpath.split("/")
	dup_fpath="%s%d%s%s" % (duplicate, cnt,"_" ,l[ len(l) - 1 ])
	print "Moving DUPLICATE FILE file: %s" % dup_fpath
	cmd = "mv " + fpath + " " + dup_fpath
	return cmd
	
def hash(dir, cnt):
	for i in os.listdir(dir):
		fpath=dir+i
		cnt = cnt + 1
		f = open(fpath)
		t = md5.new()
		t.update(f.read())
		srch = search(t.hexdigest())

		if srch:
			sum.append(t.hexdigest())
			print "file: %d, %s, %s, %s" % (cnt, t.hexdigest(), srch, fpath)
		else:
			cmd = dupname(cnt, fpath, False)
			print cmd
			os.system(cmd)

		f.close()

	return cnt

def main():
	cnt = 0
	os.system("mkdir " + duplicate)
	for list in ["./fotos/", "./fotos2/"]:
		cnt = hash(list, cnt)

if __name__ == "__main__":
	main()
