#!/usr/bin/env  python
from numpy import  *
#import utils 

class FigArray:
	"""
	see subplots

	Places several images in a user-specified array defined by the
	1-D 'gap' arrays (input) and frame widths and heights of atomic
	images (input).

	Creates the 0-1 lists required by the pylab "axis" call, and
	also in the self.axis() method, and the 0-1 x y coordinates of
	the 'gap boxes' in cease the user wishes to write various bits
	of text in the gaps (such as along the bottom row and left edge
	of the image array, or in gaps inbetween columns and rows of
	the atomic images.

	I do not use 'shape-ly' parameeterrs because it always confuses me
	since I never remember if shape[0] is along the abscissa or 
	ordinate etc...  so I use W or w for width and H or h for height
	as a mnemonic.

	On the "start at 0 or 1" question: since pylab subplots are labelled from
	1 upwards this object stars counting image rows and colums at 1.  To write
	in the first box at the bottom of the first row ask for the coordinates 
	of the box (w=1, h=1).  To write in a box to  the left of the first image of
	the first row, you will need to know the specifications of box(w=0, h=1).
	We use the saame (x,y of lower left corner, width,height of box)
	convention that the pylab 'axis()' call uses to characterize the box.
	Asking for an out-of-bounds box results in a None returned... don't
	know if this is wise.

	frame[WH] - width/height of individual image in physical units
	            (nanoinches, parsecs, furlongs etc)
	gap[wh] - interimage gap width/height numerix arrays in the same
	          length units as 'frame'.
	
	Anand Sivaramakrishnan (anand@stsci.edu) 2005
	"""

	def __init__(self, frameW, frameH, gapw, gaph):

		self.frameW = frameW
		self.frameH = frameH
		self.gapw = gapw.copy()
		self.gaph = gaph.copy()

		self.nW = len(gapw) - 1
		self.nH = len(gaph) - 1

		self.W =  self.gapw.sum() +  self.nW * self.frameW
		self.H =  self.gaph.sum() +  self.nH * self.frameH

	def dimensions(self):

		return (self.W, self.H)


	def axes(self, iw, ih):
		# iw is the count along a row, ie width-wards
		# ih is the count up a column, ie height-wards

		if (iw == 0) or (ih == 0):
			print "FigArray: WARNING!  pylab does not like zero for row or col"

		LLcornerX = (self.gapw[:iw].sum() + (iw - 1)*self.frameW)/self.W
		LLcornerY = (self.gaph[:ih].sum() + (ih - 1)*self.frameH)/self.H
		Wlength = self.frameW / self.W
		Hlength = self.frameH / self.H

		return [LLcornerX, LLcornerY, Wlength, Hlength]
	
	def display(self):
		print "  width is %.1f   height is %.1f "  %  (self.W, self.H)
		print "  %d images across by %d images high"  %  (self.nW, self.nH)
		print "  %.2f across by %.2f high atomic image"  %  (self.frameW, self.frameH)

		print " gap sum w %.2f  gap sum h %.2f" % (self.gapw.sum(),self.gaph.sum())
		
		for ii in range(self.nW):
			i = ii + 1
			print ""
			for jj in range(self.nH):
				j = jj + 1
				a = self.axes(i,j)
				print " %2d,%2d   %5.3f %5.3f  %5.3f %5.3f"  % \
				            (i,j, a[0], a[1], a[2], a[3]), 
				print "     %5.1f %5.1f  %5.1f %5.1f"  % \
				            (a[0]*self.W, a[1]*self.H, a[2]*self.W, a[3]*self.H)
			print ""
	
if __name__ == '__main__':


	frameW = 1.0
	frameH = 1.0
	gapw = array((1.0,  0.0,  0.0,  0.0,  0.0,  1.0))
	gaph = array((1.0,  0.0,  0.0,  0.0,  0.0,  1.0))

	f = FigArray(frameW, frameH, gapw, gaph)

	(W, H) = f.dimensions()
	
	for ii in range(f.nW):
		i = ii + 1
		for jj in range(f.nH):
			j = jj + 1
			a = f.axes(i,j)
			# call axis(a) here
	f.display()

  	output = """
	"""
