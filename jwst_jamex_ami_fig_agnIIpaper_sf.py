#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from FigArray import FigArray
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import sys

def plot_jwst(hatchtargets, col):

	plt.text(120,8.0,'JWST at 4.8 um', size=12, weight='bold',  color='k')
	plt.text(140,3.5,'TRUE IMAGING', size=8, weight='bold', color=col[0])
	plt.text(140,5.5,   'MODEL FITTING', size=8, weight='bold', color=col[0])
	if hatchtargets:
		jw_ext = a.add_patch( Polygon([[71,cmin],[571,cmin],[571,5.0],[71,5.0]],
		                              closed=True, fill=True, color=col[0], alpha=col[1] ))
		jw_bin = a.add_patch( Polygon([[71,cmin],[571,cmin],[571,10.0],[71,10.0]],
	                              closed=True, fill=True, color=col[0], alpha=col[2] ))
	else:
		jw_ext = a.add_patch( Polygon([[71,cmin],[571,cmin],[571,5.0],[71,5.0]],
		                              closed=True, fill=False, color=col[0], alpha=col[2], hatch='//' ))
		jw_bin = a.add_patch( Polygon([[71,cmin],[571,cmin],[571,10.0],[71,10.0]],
		                              closed=True, fill=False, color=col[0], alpha=col[2], hatch='\\\\' ))
	return None

def condition_plotaxes(ax):
	ax.set_xscale("log")
	ax.yaxis.set_major_locator( MultipleLocator(5) )
	xmajorFormatter = FormatStrFormatter('%.0f mas')
	ax.spines['top'].set_visible(False)
	ax.xaxis.set_major_formatter( xmajorFormatter )
	ax.tick_params(axis='both', which='major', labelsize=8)

def physicaldistance_axis(ax, span, s):
	""" span = sep_au tuple or sep_pc tuple.  
	    s is 'au' or 'pc'"""
	colr = 'blue'
	a2 = ax.twiny()
	a2.yaxis.set_major_locator(NullLocator())
	plt.xlim(span)
	a2.set_xscale("log")
	fmtstr = "%.0f " + s
	xmajorFormatter = FormatStrFormatter(fmtstr)
	####  does not have any effect a2.spines['top'].set_linewidth(20.0)
	a2.spines['top'].set_color(colr)
	a2.xaxis.label.set_color(colr)
	a2.tick_params(axis='x', colors=colr)
	a2.xaxis.set_major_formatter( xmajorFormatter )
	a2.axhline(y=13, c='b', lw=2)
	a2.tick_params(axis='both', which='major', labelsize=8)

def mas2pc(mas, Dphysical):
	""" at a distance Dphysical so many mas is this many of the sme unit """
	angle_in_rad = (mas / 1000.0) / 206264.8
	return Dphysical * angle_in_rad


if __name__ == "__main__":

	HATCHTARGETS = False
	# Either hatch targets or hatch telescope# the 'other' gets colors

	frameW = 5.0
	frameH = 1.5
	gaph = np.array( (0.55, 0.4, 0.4, 0.4, 0.65) )
	gapw = np.array( (1.0, 0.25) )
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	nW, nH = fig.nW, fig.nH

	# res in mas, contrast in mag
	resolution, contrast = ((30,1300), (0, 13))
	rmin, rmax = resolution
	cmin, cmax = contrast
	#color scheme (color,transparency/alpha)
	targetname = 'red'

	if HATCHTARGETS:
		physicalobject = '0.3'
		indskh='/'
		oudskh='\\'
		torush='|'
		fuelh='/'
		grlnh='#'
		jw=('blue',0.2,0.1)
	else:
		physicalobject = 'g'
		# next 4 lines are old style - delete later
		indsk=(physicalobject,0.25)
		oudsk=(physicalobject,0.2)
		torus=(physicalobject,0.15)
		fuel=(physicalobject,0.05)
		jw=('blue',0.5,0.3)

	plot = plt.figure(1, figsize=(W, H))

	row = 3  ##########  M31
	D = 0.8e6 #pc
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)

	# special xlabel top row
	plt.text(34, 16.0, 'Regions probed by JWST NIRISS AMI with F480M', size=12.0, weight='bold')

	plt.text(22.0,8.0,r' M31 ', size=12.0, style='italic', weight='bold', color=targetname, rotation=90)
	plt.text(190,11.0,'FUEL, STRUCTURE, FEEDBACK', size=10, color=physicalobject, style='italic', weight='bold')
	plt.text(40,11.0,'TORUS', size=10, color=physicalobject, style='italic', weight='bold')

	# special center Y label in mid-row
	plt.text(17, -7.0, 'Contrast / magnitudes', size=12.0, rotation=90, weight='bold')

	if HATCHTARGETS:
		a.axvspan(170,rmax, fill=False, hatch=fuelh, alpha=0.3)
		a.axvspan(rmin,170, fill=False, hatch=torush, alpha=0.3)
	else:
		a.axvspan(100,rmax, fill=True, color=fuel[0], alpha=fuel[1])
		a.axvspan(rmin,100, fill=True, color=torus[0], alpha=torus[1])

	plot_jwst(HATCHTARGETS, jw)

	condition_plotaxes(a)
	sep_pc = (mas2pc(rmin, D), mas2pc(rmax, D))
	physicaldistance_axis(a, sep_pc, 'pc')

	row = 2 ######### N1068
	D = 12.7e6 # pc
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)

	#lt.text(22.0,8.0,r'Sgr A*', size=12.0, style='italic', weight='bold', color=targetname, rotation=90)
	plt.text(22.0,8.0,r'N1068', size=12.0, style='italic', weight='bold', color=targetname, rotation=90)
	plt.text(120, -53.0, 'Separation', size=12.0, weight='bold')

	#lt.text(???,11.0,'FUEL, STRUCTURE, FEEDBACK??', size=10, color=physicalobject, style='italic', weight='bold')  # FIXME
	plt.text(200,11.0,'FUEL, STRUCTURE, FEEDBACK', size=10, color=physicalobject, style='italic', weight='bold')
	plt.text(32,11.0,'TORUS', size=10, color=physicalobject, style='italic', weight='bold') 

	if HATCHTARGETS:
		a.axvspan(49,rmax, fill=False, hatch=fuelh, alpha=0.3)  
		a.axvspan(rmin,49, fill=False, hatch=torush, alpha=0.3) 
	else:
		a.axvspan(49,rmax, fill=True, color=fuel[0], alpha=fuel[1]) 
		a.axvspan(rmin,49, fill=True, color=torus[0], alpha=torus[1]) 

	plot_jwst(HATCHTARGETS, jw)

	condition_plotaxes(a)
	sep_pc = (mas2pc(rmin, D), mas2pc(rmax, D))
	physicaldistance_axis(a, sep_pc, 'pc')



	row = 1  ##########  N4151
	D = 17.0e6 # Mpc
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)

	plt.text(22.0,8.0,r'N4151', size=12.0, style='italic', weight='bold', color=targetname, rotation=90)
	plt.text(40,11.0,'FUEL, STRUCTURE, FEEDBACK', size=10, color=physicalobject, style='italic', weight='bold')

	if HATCHTARGETS:
		a.axvspan(rmin,rmax, fill=False, hatch=fuelh, alpha=0.3)
	else:
		a.axvspan(rmin,rmax, fill=True, color=fuel[0], alpha=fuel[1])

	plot_jwst(HATCHTARGETS, jw)

	condition_plotaxes(a)
	sep_pc = (mas2pc(rmin, D), mas2pc(rmax, D))
	physicaldistance_axis(a, sep_pc, 'pc')


	row = 0  ##########  3C273
	D = 650.0e6 #pc
	a = plt.axes(fig.axes(1,row+1))
	plt.setp(a, xlim=resolution,  ylim=contrast)

	plt.text(22.0,8.0,r'3C273', size=12.0, style='italic', weight='bold', color=targetname, rotation=90)
	plt.text(40,11.0,'FUEL, STRUCTURE, FEEDBACK', size=10, color=physicalobject, style='italic', weight='bold')

	if HATCHTARGETS:
		a.axvspan(rmin,rmax, fill=False, hatch=fuelh, alpha=0.3)
	else:
		a.axvspan(rmin,rmax, fill=True, color=fuel[0], alpha=fuel[1])

	plot_jwst(HATCHTARGETS, jw)

	condition_plotaxes(a)
	sep_pc = (mas2pc(rmin, D), mas2pc(rmax, D))
	physicaldistance_axis(a, sep_pc, 'pc')

	plt.savefig("jwst_jamex_ami_angIIpaper.pdf", dpi=150)
