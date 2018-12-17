import pdb
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import sys

class FigArray:
	"""
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

def plot_afta(cmin, col):
	plt.text(20, 1,'AFTA at 0.4 um', size=10, weight='bold',  color='k', style='italic')
	plt.text(32,5.5,'True imaging',  size=8, weight='bold', color='0.2')
	plt.text(32,7.8,'Model fitting', size=8, weight='bold', color='0.2')
	vertices = ([[17,cmin],[136,cmin],[136,7.0],[17,7.0]],
	            [[17,cmin],[136,cmin],[136,12.0],[17,12.0]])
	a.add_patch( Polygon(vertices[0], closed=True, fill=True, color=col[0], alpha=col[2] ))
	a.add_patch( Polygon(vertices[1], closed=True, fill=False, color=col[0], alpha=col[1], hatch='//' ))
	a.add_patch( Polygon(vertices[0], closed=True, fill=False, edgecolor=col[0], alpha=0.5 ))
	a.add_patch( Polygon(vertices[1], closed=True, fill=False, edgecolor=col[0] ))

def plot_jwst(cmin, col):
	plt.text(140,1.0,'JWST at 4.8 um', size=10, weight='bold',  color='k', style='italic')
	plt.text(160,3.5,'True imaging',  size=8, weight='bold', color='0.2')
	plt.text(160,5.8,'Model fitting', size=8, weight='bold', color='0.2')
	vertices = ([[71,cmin],[571,cmin],[571,5.0], [71,5.0]],
	            [[71,cmin],[571,cmin],[571,10.0],[71,10.0]])
	a.add_patch( Polygon(vertices[0], closed=True, fill=True, color=col[0], alpha=col[2] ))
	a.add_patch( Polygon(vertices[1], closed=True, fill=False, color=col[0], alpha=col[1], hatch='\\\\' ))
	a.add_patch( Polygon(vertices[0], closed=True, fill=False, edgecolor=col[0], alpha=0.5 ))
	a.add_patch( Polygon(vertices[1], closed=True, fill=False, edgecolor=col[0] ))
	return None

def plot_atlast(cmin, col):
	plt.text(3.2,1.0,'ATLAST at 0.5 um', size=10, weight='bold',  color='k',style='italic')
	plt.text(3.5,5.5,'True imaging',  size=8, weight='bold', color='0.2')
	plt.text(3.5,7.8,'Model fitting', size=8, weight='bold', color='0.2')
	vertices = ([[3.1,cmin],[30,cmin],[30,7.0], [3.1,7.0]],
	            [[3.1,cmin],[30,cmin],[30,12.0],[3.1,12.0]])

        #.add_patch( Polygon(vertices[0], closed=True, fill=False, color=col[0], alpha=col[1], hatch='/' ))
	a.add_patch( Polygon(vertices[0], closed=True, fill=True, color=col[0], alpha=col[2] ))
        a.add_patch( Polygon(vertices[1], closed=True, fill=False, color=col[0], alpha=col[1], hatch='\\\\' ))
        a.add_patch( Polygon(vertices[0], closed=True, fill=False, edgecolor=col[0], alpha=0.5 ))
        a.add_patch( Polygon(vertices[1], closed=True, fill=False, edgecolor=col[0] ))
	return None

def condition_plotaxes(ax):
	ax.set_xscale("log")
	ax.yaxis.set_major_locator( MultipleLocator(5) )
	ax.xaxis.set_tick_params(width=2)
	ax.yaxis.set_tick_params(width=2)

	xmajorFormatter = FormatStrFormatter('%.0f mas')
	ax.spines['top'].set_visible(False)
	ax.xaxis.set_major_formatter( xmajorFormatter )
	ax.tick_params(axis='both', which='major', labelsize=8)


def physicaldistance_axis(a2, xspan, yspan, s, fmtprec = None):
	""" span = sep_au tuple or sep_pc tuple.  
	    s is 'au' or 'pc'"""
	#pdb.set_trace()
	colr = 'g'
	plt.xlim(xspan)
	a2.yaxis.set_major_locator(NullLocator())
	a2.set_xscale("log")
	a2.xaxis.set_tick_params(width=2)
	if fmtprec is not None:
		fmtstr = "%.001f " + s
	else:
		fmtstr = "%.0f " + s
	xmajorFormatter = FormatStrFormatter(fmtstr)
	a2.spines['top'].set_color(colr)
	a2.xaxis.label.set_color(colr)
	a2.tick_params(axis='x', colors=colr)
	a2.xaxis.set_major_formatter( xmajorFormatter )
	a2.axhline(y=yspan[1], c=colr, lw=2)
	a2.tick_params(axis='both', which='major', labelsize=8)


def mas2pc(mas, Dphysical):
	""" at a distance Dphysical so many mas is this many of the sme unit """
	angle_in_rad = (mas / 1000.0) / 206264.8
	return Dphysical * angle_in_rad


def bugfix_twiny_nukes_old_y_labels_and_ticks(xlim=None,  ylim=None):
	""" Hardwire a few ticks on the y axis...
	"""
	dx = 0.05
	plt.plot((xlim[0],xlim[0]+dx), (5,5),   lw=0.5, ls="-", c='k', marker=None)
	plt.plot((xlim[0],xlim[0]+dx), (10,10), lw=0.5, ls="-", c='k', marker=None)
	plt.text(0.85, 4.5,   "5", color='k', fontsize=8)
	plt.text(0.8, 9.5, "10", color='k',fontsize=8)



if __name__ == "__main__":


	frameW = 5.0
	frameH = 1.4
	gaph = np.array( (0.55, 0.4, 0.4, 0.4, 0.65) )
	gapw = np.array( (0.65, 0.35) )
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	nW, nH = fig.nW, fig.nH

	print "figure width = ", W, "  height = ", H

	resolution, contrast = ((1,1010), (0, 15))
	rmin, rmax = resolution
	targetcolor = 'm'
	targetfactor = 0.65 # divide or mult a limit to offset by same amounts in log scale
	targetfontsize = 16
	targetheight = 7

	physicalobject = 'g'
	# next 4 lines are old style - delete later
	indsk = (physicalobject,0.15)
	oudsk = (physicalobject,0.1)
	torus = (physicalobject,0.05)
	fuel = (physicalobject,0.025)
	af = ('blue',0.3,0.1)
	jw = ('red',0.3,0.1)
        at = ('black',0.3,0.1)
	plot = plt.figure(1, figsize=(W, H))

	row = 3 ######### SAG A*
	target = 'Sgr A*'
	D = 8000.0 # pc
	sep_au = (206264.8*mas2pc(rmin, D), 206264.8*mas2pc(rmax, D))
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)
	plt.text(0.65, 18, 'AGN search spaces for JWST, AFTA & ATLAST NRM', size=14.0,
	         weight='bold')
	plt.text(255, 16.3, 'Credit: The JAMex Team', size=6.0, style='italic')
	plt.text(255, 15.3, 'with NASA APRA support', size=6.0, style='italic')

	plt.text(resolution[0]/targetfactor, targetheight, target, size=targetfontsize,
	         style='italic', weight='bold', color=targetcolor, rotation=90)
	plt.text(resolution[0]*0.6, -10, 'Contrast (magnitudes)', size=12.0,
	         rotation=90, weight='bold')

	plt.text(300,contrast[1]-2,'TORUS', size=10, 
	         color=physicalobject, style='italic', weight='bold')
	plt.text(20,contrast[1]-2,'OUTER DISK', size=10, 
	         color=physicalobject, style='italic', weight='bold')
	plt.text(1.5,contrast[1]-2,'INNER', size=10, color=physicalobject, style='italic', weight='bold')
	plt.text(1.5,contrast[1]-4,'DISK', size=10, color=physicalobject, style='italic', weight='bold')
	a.axvspan(100,rmax, fill=True, color=torus[0], alpha=torus[1])
	a.axvspan(rmin,100, fill=True, color=oudsk[0], alpha=oudsk[1])
	a.axvspan(rmin,10, fill=True, color=indsk[0], alpha=indsk[1])
	plot_jwst(contrast[0], jw)
	plot_afta(contrast[0], af)
	plot_atlast(contrast[0],at)
	condition_plotaxes(a)
	bugfix_twiny_nukes_old_y_labels_and_ticks(xlim=resolution,  ylim=contrast)
	atwin = a.twiny()
	physicaldistance_axis(atwin, sep_au, contrast, 'AU')



	row = 2  ##########  M31
	target = "M31"
	D = 0.8e6 #pc
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)

	plt.text(resolution[0]/targetfactor, targetheight-2.5, target, size=targetfontsize,
	         style='italic', weight='bold', color=targetcolor, rotation=90)
	plt.text(20,contrast[1]-2,'TORUS', size=10, color=physicalobject, style='italic', weight='bold')
	plt.text(300,contrast[1]-2,'FUEL', size=10, 
	         color=physicalobject, style='italic', weight='bold')
	plt.text(2.5,contrast[1]-2,'OUTER DISK', size=10, 
	         color=physicalobject, style='italic', weight='bold')
	a.axvspan(170,rmax, fill=True, color=fuel[0], alpha=fuel[1])
	a.axvspan(17,170, fill=True, color=torus[0], alpha=torus[1])
	a.axvspan(1.7,17, fill=True, color=oudsk[0], alpha=oudsk[1])
	a.axvspan(rmin,1.7, fill=True, color=indsk[0], alpha=indsk[1])
	plot_jwst(contrast[0], jw)
	plot_afta(contrast[0], af)
	plot_atlast(contrast[0],at)
	condition_plotaxes(a)
	bugfix_twiny_nukes_old_y_labels_and_ticks(xlim=resolution,  ylim=contrast)
	atwin = a.twiny()
	sep_pc = (mas2pc(rmin, D), mas2pc(rmax, D))
	physicaldistance_axis(atwin, sep_pc, contrast, 'pc', fmtprec=777)
#	physicaldistance_axis(atwin, sep_pc, contrast, 'pc', fmtprec=None)


	row = 1  ##########  N4151
	target = "N4151"
	D = 17.0e6 # Mpc
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)

	plt.text(resolution[0]/targetfactor, targetheight, target, size=targetfontsize,
	         style='italic', weight='bold', color=targetcolor, rotation=90)
	plt.text(40,contrast[1]-2,'FUEL, STRUCTURE, FEEDBACK', size=10, color=physicalobject, style='italic', weight='bold')
	plt.text(2.5,contrast[1]-2,'TORUS', size=10, 
	         color=physicalobject, style='italic', weight='bold')
	a.axvspan(12,rmax, fill=True, color=fuel[0], alpha=fuel[1])
	a.axvspan(1.2,12, fill=True, color=torus[0], alpha=torus[1])
	a.axvspan(rmin,1.2, fill=True, color=oudsk[0], alpha=oudsk[1])

	plot_jwst(contrast[0], jw)
	plot_afta(contrast[0], af)
	plot_atlast(contrast[0],at)
	condition_plotaxes(a)
	bugfix_twiny_nukes_old_y_labels_and_ticks(xlim=resolution,  ylim=contrast)
	sep_pc = (mas2pc(rmin, D), mas2pc(rmax, D))
	atwin = a.twiny()
	# BUGDEMO - call this routine for the next row...  the original a.yaxis labels get wiped out!!!!
	physicaldistance_axis(atwin, sep_pc, contrast, 'pc',fmtprec=777)


	row = 0  ##########  3C273
	target = "3C273"
	D = 650.0e6 #pc
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)

	plt.text(resolution[0]/targetfactor, targetheight, target, size=targetfontsize,
	         style='italic', weight='bold', color=targetcolor, rotation=90)
	plt.text(40,contrast[1]-2,'FUEL, STRUCTURE, FEEDBACK', size=10, color=physicalobject, style='italic', weight='bold')

	a.axvspan(rmin,rmax, fill=True, color=fuel[0], alpha=fuel[1])

	plot_jwst(contrast[0], jw)
	plot_afta(contrast[0], af)
	plot_atlast(contrast[0],at)
	condition_plotaxes(a)
	bugfix_twiny_nukes_old_y_labels_and_ticks(xlim=resolution,  ylim=contrast)
	sep_pc = (mas2pc(rmin, D), mas2pc(rmax, D))
	atwin = a.twiny()
	physicaldistance_axis(atwin, sep_pc, contrast, 'pc')

	plt.text(50, -4.0, 'Separation', size=12.0, weight='bold')
plt.savefig("/Users/barrymckernan/Documents/Documents/Documents/papers/nrm/agn_paper/test_agn_fig.pdf", dpi=150)
plt.show()
