import sys, os, time
import numpy as np
import scipy.special
from scipy import signal
from astropy.io import fits
import math
from FigArray import FigArray
import numpy as np
import pylab as plt
import gc
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import string

from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D


LOC = '/Users/kstlaurent/NIRISS NRM/'

OBJECT_FILE = 'Objects/binobj_L%.1f_C%.1f.fits'#(NL, C)

object_plot = 'Plots/objects.pdf'#(pup,ff,phot)

PUPILS = ['MASK_NRM','CLEARP']
FLAT_FIELD_ERROR = [0.00,0.01,0.03]

LENGTH = [1.0,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0,3.0,4.0,5.0]

Nphotons = [1E7]#,1E4,1E5,1E6,1E7]

PWR = 0.15
CLP = .8
ov = 11
fov = 81


def grab_files():
	
	objlist = []
	objmaxlist = []
	
	for NL in LENGTH:
		for C in CONTRAST:
				obj = fits.getdata(LOC+OBJECT_FILE%(NL,C))[::-1,:]
	
				print OBJECT_FILE%(NL,C)
	
				objlist.append(obj)
				objmaxlist.append(obj.max())
			
	return objlist, objmaxlist
	
def PlotOutput():
	
	x = len(LENGTH)
	y = len(CONTRAST)
	
	frameW = 1.5
	frameH = 1.5
	gapw = 0.05*np.ones(x+1)
	gapw[0] = 0.30
	gaph = 0.05*np.ones(y+1)
	#gaph[0] = 0.30
	gaph[4] = 0.30
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	objlist, objmaxlist = grab_files()

	ctr = 0
	

	plt.text(-0.1,1.09, "L = 1.0 pix", fontsize=14, rotation=0, color='k')
	plt.text(0.11,1.09, "L = 1.5 pix", fontsize=14, rotation=0, color='k')
	plt.text(0.32,1.09, "L = 2.0 pix", fontsize=14, rotation=0, color='k')
	plt.text(0.53,1.09, "L = 2.5 pix", fontsize=14, rotation=0, color='k')
	plt.text(0.74,1.09, "L = 3.0 pix", fontsize=14, rotation=0, color='k')
	plt.text(0.95,1.09, "L = 4.0 pix", fontsize=14, rotation=0, color='k')
		
	plt.text(-0.152,1, "C = 5 mag", fontsize=14, rotation=90, color='k')
	plt.text(-0.152,0.7, "C = 4 mag", fontsize=14, rotation=90, color='k')
	plt.text(-0.152,0.4, "C = 3 mag", fontsize=14, rotation=90, color='k')
	plt.text(-0.152,0.1, "C = 2 mag", fontsize=14, rotation=90, color='k')
	
	#plt.text(0.2,-0.11, "Detector Scale Truth Model", fontsize=16, rotation=0, color='k')
		
	
	plt.axis("off")
	
	
	for i in range(x):
		for j in range(y):
			
			dispim = np.power(objlist[ctr],PWR)
			dispim = dispim[35:45,35:45]
			
			objmax = np.power(objmaxlist[ctr],PWR)
	
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,j+1))
		
			#plt.text(0.1,6, "length = %.2f" %(LENGTH[i]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1,13, "C = %.1f" %(CONTRAST[j]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1, 20, "i = %d, j = %d"%(i,j), fontsize=5, rotation=0, color='y')
			#plt.text(0.1, 25, "ctr = %d"%(ctr), fontsize=5, rotation=0, color='y')
			
			
			p = plt.imshow(dispim,vmax = objmax,vmin=0,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			
			
	
			ctr += 1
	
	
	
	plt.savefig(LOC+object_plot%(), dpi=150)
	plt.close()
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	PlotOutput()
	
	
				
		
if __name__ == "__main__":
	
	main()