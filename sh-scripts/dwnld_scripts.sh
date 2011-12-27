function dwnld_ngspace () {
	for ((i=1;i<15;i++)) do if [ "$?" -ne 0 ]; then echo "no files there";  break; fi; wget "http://www.nangaspace.com/upload/2010-02-24-01-0$i.jpg"; done;
}
