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

ESTIM_FILE = 'Estim/%s_OPD162_ff%.2f_L%.2f_C%.1f_N%.0E_noisy_estim.fits'#(pup, ff, NL, C, Nphot)

estim_plot = 'Plots/NoisyEstimBars_%s_OPD162_ff%.2f_N%.0E.pdf'#(pup,ff,phot)

PUPILS = ['MASK_NRM','CLEARP']
FLAT_FIELD_ERROR = [0.00,0.01,0.03]

LENGTH = [1.0,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0,3.0,4.0,5.0]

Nphotons = [1E7]#,1E4,1E5,1E6,1E7]

PWR = 0.15
CLP = .8
ov = 11
fov = 81


def grab_files(pup,ff,Nphot):
	
	estimlist = []
	estimmaxlist = []
	
	for NL in LENGTH:
		for C in CONTRAST:
				estim = fits.getdata(LOC+ESTIM_FILE%(pup,ff,NL,C,Nphot))[::-1,:]
	
				print ESTIM_FILE%(pup,ff,NL,C,Nphot)
	
				estimlist.append(estim)
				estimmaxlist.append(estim.max())
			
	return estimlist, estimmaxlist
	
def PlotOutput(pup,ff,Nphot):
	
	x = len(LENGTH)
	y = len(CONTRAST)
	
	frameW = 1.5
	frameH = 1.5
	gapw = 0.05*np.ones(x+1)
	gapw[0] = 0.30
	gaph = 0.05*np.ones(y+1)
	gaph[0] = 0.30
	gaph[4] = 0.30
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	estimlist, estimmaxlist = grab_files(pup,ff,Nphot)

	ctr = 0
	

	if pup == 'MASK_NRM':
		plt.text(0.2,-0.11, "NIRISS NRM    ff = %.2f    Nphot = %.0E"%(ff,Nphot), fontsize=16, rotation=0, color='k')
		plt.text(-0.1,1.09, "L = 1.0 pix", fontsize=14, rotation=0, color='k')
		plt.text(0.11,1.09, "L = 1.5 pix", fontsize=14, rotation=0, color='k')
		plt.text(0.32,1.09, "L = 2.0 pix", fontsize=14, rotation=0, color='k')
		plt.text(0.53,1.09, "L = 2.5 pix", fontsize=14, rotation=0, color='k')
		plt.text(0.74,1.09, "L = 3.0 pix", fontsize=14, rotation=0, color='k')
		plt.text(0.95,1.09, "L = 4.0 pix", fontsize=14, rotation=0, color='k')
		
	else:
		plt.text(0.2,-0.11, "NIRCam Clear    ff = %.2f    Nphot = %.0E"%(ff,Nphot), fontsize=16, rotation=0, color='k')
		
	if ff == 0:
		plt.text(-0.152,1, "C = 5 mag", fontsize=14, rotation=90, color='k')
		plt.text(-0.152,0.7, "C = 4 mag", fontsize=14, rotation=90, color='k')
		plt.text(-0.152,0.4, "C = 3 mag", fontsize=14, rotation=90, color='k')
		plt.text(-0.152,0.1, "C = 2 mag", fontsize=14, rotation=90, color='k')
		
	
	plt.axis("off")
	
	
	for i in range(x):
		for j in range(y):
			
			dispim = np.power(estimlist[ctr],PWR)
			dispim = dispim[35:45,35:45]
			
			estimmax = np.power(estimmaxlist[ctr],PWR)
	
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,j+1))
		
			#plt.text(0.1,6, "length = %.2f" %(LENGTH[i]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1,13, "C = %.1f" %(CONTRAST[j]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1, 20, "i = %d, j = %d"%(i,j), fontsize=5, rotation=0, color='y')
			#plt.text(0.1, 25, "ctr = %d"%(ctr), fontsize=5, rotation=0, color='y')
			
			
			p = plt.imshow(dispim,vmax = estimmax,vmin=0,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			
			
	
			ctr += 1
	
	
	
	plt.savefig(LOC+estim_plot%(pup,ff,Nphot), dpi=150)
	plt.close()
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	for pup in PUPILS:
		for ff in FLAT_FIELD_ERROR:
			for Nphot in Nphotons:
				PlotOutput(pup,ff,Nphot)
	
	
				
		
if __name__ == "__main__":
	
	main()