import sys, os, time
import numpy as np
import scipy.special
from scipy import signal
from astropy.io import fits
import math
from FigArray import FigArray
import numpy as np
import pylab as plt
import pyfits
import gc
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import string
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D

LOC = '/Users/kstlaurent/Box Sync/NIRISS NRM/'

NEW_OBJECT_FILE = 'New Object/%s_OPD%d_ff%.2f_L%.2f_C%.2f.fits'#(pup,OPD,ff,L,C)'

newobj_plot = 'Plots/NewOBJ_%s_%d_%.2f.pdf'

LENGTH = [1.0,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0,3.0,4.0,5.0]
PUPILS = ['CLEARP','MASK_NRM']
OP_PATH_DIFF = [162,810]
FLAT_FIELD_ERROR = [0.00,0.01,0.03]

PWR = 0.25
CLP = .7
Nphotons = 1E8
ov = 11
fov = 81


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
plotting the 'new objects'
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def grab_files(pup,opd,ff):

	newobjlist = []
	newobjmaxlist = []
	newobjminlist = []
	
	for NL in LENGTH:
		for C in CONTRAST:
			
			new_obj = fits.getdata(LOC+NEW_OBJECT_FILE%(pup,opd,ff,NL,C))
			newobjlist.append(new_obj)
			newobjmaxlist.append(new_obj.max())
			newobjminlist.append(new_obj.min())
			
	return newobjlist,newobjmaxlist,newobjminlist
	
def PlotOutput(pup,opd,ff):
	
	x = len(LENGTH)
	y = len(CONTRAST)
	
	frameW = 0.95
	frameH = 0.95
	gapw = 0.05*np.ones(x+1)
	gaph = 0.05*np.ones(y+1)
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	newobjlist,newobjmaxlist,newobjminlist = grab_files(pup,opd,ff)

	ctr = 0
	
	for i in range(x):
		for j in range(y):
			
			dispim = np.power(newobjlist[ctr],PWR)
			dispim = dispim[35:46,35:46]
			
			objmax = np.power(newobjmaxlist[ctr],PWR)
			objmin = np.power(newobjminlist[ctr],PWR)
	
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,j+1))
		
			plt.text(0,1, "L = %.2f NIRISS Pixels" %(LENGTH[i]), fontsize=5, rotation=0, color='w')
			plt.text(0,0, "C = %.1f mag" %(CONTRAST[j]), fontsize=5, rotation=0, color='w')
			p = plt.imshow(dispim,vmax = objmax,vmin=objmin,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1

	plt.savefig(LOC+newobj_plot%(pup,opd,ff), dpi=150)
	plt.close()
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	for pup in PUPILS:
		for opd in OP_PATH_DIFF:
			for ff in FLAT_FIELD_ERROR:
				print pup,opd,ff,'plotting...'		
				PlotOutput(pup,opd,ff)
				print pup,opd,ff,'done'
				
		
if __name__ == "__main__":
	
	main()