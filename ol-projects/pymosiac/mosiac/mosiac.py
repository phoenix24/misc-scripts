#!/usr/bin/python

import sys, math, os, os.path, time
import pickle, Image
from threading import Thread

THUMBNAIL_SIZE = (2,2)
THUMBNAIL_NAME = "thmb_%d.jpeg"
THUMBNAIL_PALLETTE = {}


class process_image(Thread):
	""" """
	def __init__(self, image, resize, outputdir):
		""" intialize the process thread. """
		Thread.__init__(self)
		self.resize = resize
		self.avgcolor = 0
		self.imagename = image

		try:
			print "forking thread ", self.name
			self.image = Image.open(os.path.join(outputdir, image))
			self.output = os.path.join(outputdir, "thumbnails/%s" % image)
			self.image_avg()
			self.image_resize()
		except IOError:
			print "invalid input image."

	def image_avg(self):
		""" calculate the image average; based on a screwed up algorithm i cameup with. """
		imgdata = list(self.image.getdata())
		r, g, b, size = 0, 0, 0, len(imgdata)
		for i in imgdata:
			r, g, b = i[0]+r, i[1]+g, i[2]+b
	
		r, g, b = r/size, g/size, b/size
		self.avgcolor =  (r+g+b)/3

	def image_resize(self):
		""" resize the given image to the designated thumbnail size. """
		self.image.resize(self.resize).save(self.output, "jpeg")


class mosiac():
	""" mosiac application class. contains all the helper functions to create a mosiac. """

	def __init__(self, image, imagedir, output):
		""" initialize the mosiac application class. """
		self.moziac = ''
		self.outfile = output
		self.imagedir = imagedir
		self.thumbnail = THUMBNAIL_SIZE
		self.imagequeue = []
		self.imagepallette = {}

		try:
			self.image = Image.open(os.path.join(imagedir, image))
		except IOError:
			print "invalid input image."
		
		self.scandir()

	def scandir(self):
		""" scan the image directory, and for each jpeg image, fork a seprate thread calculating its average. """

		dirlist = [ f for f in os.listdir(self.imagedir) if os.path.isfile(os.path.join(self.imagedir, f))]
		for image in dirlist:
			current = process_image(image, self.thumbnail, self.imagedir)
			self.imagequeue.append(current)
			current.start()

		for image in self.imagequeue:
			image.join()
			print "image-pallette : ", image.avgcolor, image.imagename
			self.imagepallette[image.avgcolor] = image.imagename


	def image_search(self, col):
		""" find the image tile (from the image directory) closest to the current image tile at hand,"""

		tmp, limit = 0, 100
		col = (col[1] + col[1] + col[2]) / 3

		for i in self.imagepallette:
			diff = abs(col-i)
			if diff < limit and diff < limit:
				tmp, limit = i, diff
		return self.imagepallette [ tmp ] 


	def get_color(xy, gridsize):
		""" find the average color of an image, my-screwed up alogorithm. """
		rr,gg,bb =0, 0, 0
		for i in range(gridsize):
			for j in range(gridsize):
				r,g,b = self.image.gelpixel((xy[0]+j,xy[1]+i))
				rr, gg, bb = r+rr, g+gg, b+bb
		return (rr+gg+bb)/(gridsize*3)


	def create(self):
		""" take it on! all is well; create the mosiac """
#		self.moziac = Image.new("RGBA", (self.image.size[0]*3, self.image.size[1]*3))
		self.moziac = Image.new("RGBA", (self.image.size[0], self.image.size[1]))
		data = list(self.image.getdata())
		X, Y = self.image.size[0], self.image.size[1]
		x, y = 0, 0
		for col in data:
			x += 3
			if x >= X*3:
				x, y = 0, y + 3
			
			img = self.image_search(col)
			img = "thumbnails/%s" % img
			img = os.path.join(self.imagedir, img)
			try:
				img = Image.open(img)
				self.moziac.paste(img, (x, y))
			except IOError:
				print "IOError occured while opening the file"
				pass
	
	def save(self):
		""" helper function to save the mosiac. """
		self.outfile = os.path.join(self.imagedir, "test")
		self.moziac.save(self.outfile, "jpeg")

	def show(self):
		""" helper function to show the created mosiac. """
		self.moziac.show()


if __name__ == '__main__':
	#must put proper input parser.
	if len(sys.argv) < 2:
		print "usage : ./main <input-file>  <input-directory>"
		sys.exit(-1)
	
	iDir   = sys.argv[2]
	if not os.path.isdir(iDir):
		print "directory is required as second input. "
		sys.exit(-1)

	iImage = sys.argv[1]
	if not os.path.isfile(iImage):
		print "input image must be a file, as first input. "
		sys.exit(-1)
	
	moz = mosiac(iImage, iDir, "test.jpeg")
	moz.create()
	moz.save()
	moz.show()

