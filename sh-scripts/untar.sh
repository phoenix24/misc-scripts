#!/usr/bin/bash

for i in `ls *.gz`
do 
	echo "untarring $i"
	tar xf $i
done
