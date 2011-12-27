#!/usr/bin/bash

for i in `ls`
do
	echo "tarring $i currently"
	tar czf "$i.tar.gz" $i
done
