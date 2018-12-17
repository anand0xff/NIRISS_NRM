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

ESTIM_FILE = 'N1068_Estim/%s_OPD162_ff%.2f_F430M_N1068_N%0.E_noisy_bar%.1f.fits'#(pup,ff,phot)


estim_plot = 'N1068_Plots/NoisyEstimBars_%s_ff%.2f_162.pdf'#(pup,ff)

PUPILS = ['MASK_NRM','CLEARP']
BAR_BRIGHTNESS = [0.0,0.3,1.0]
Nphotons = [1E8,1E7]
FLAT_FIELD_ERROR = [0.00,0.01]

PWR = 0.15
CLP = .8
ov = 11
fov = 81


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
plotting the metric 'map'
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def grab_files(pup,ff):
	
	estimlist = []
	estimmaxlist = []
	estimminlist = []
	
	
	for bright in BAR_BRIGHTNESS:
		for phot in Nphotons:
				estim = fits.getdata(LOC+ESTIM_FILE%(pup,ff,phot,bright))[::-1,:]
	
				print ESTIM_FILE%(pup,ff,phot,bright)
	
				estimlist.append(estim)
				estimmaxlist.append(estim.max())
				estimminlist.append(estim.min())
			
	return estimlist, estimmaxlist,estimminlist
	
def PlotOutput(pup,ff):
	
	x = len(BAR_BRIGHTNESS)
	y = len(Nphotons)
	
	frameW = 1.5
	frameH = 1.5
	gapw = 0.05*np.ones(x+1)
	gapw[0] = 0.2
	gaph = 0.05*np.ones(y+1)
	gaph[2] = 0.2
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	estimlist, estimmaxlist,estimminlist = grab_files(pup,ff)

	ctr = 0
	
	plt.text(0.03,1.06, "no bar", fontsize=10, rotation=0, color='k')
	plt.text(0.32,1.06, "30% ring brightness", fontsize=10, rotation=0, color='k')
	plt.text(0.76,1.06, "equal brightness", fontsize=10, rotation=0, color='k')
	plt.text(-0.155,0.85, "$10^7$ photons", fontsize=10, rotation=90, color='k')
	plt.text(-0.155,0.3, "$10^8$ photons", fontsize=10, rotation=90, color='k')
	plt.axis("off")
	
	
	for i in range(x):
		for j in range(y):
			
			dispim = np.power(estimlist[ctr],PWR)
			dispim = dispim[36:46,36:46]
			
			estimmax = np.power(estimmaxlist[ctr],PWR)
	
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,j+1))
		
			#plt.text(0.1,6, "brightness = %.1f" %(BAR_BRIGHTNESS[i]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1,13, "%.0E" %(Nphotons[j]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1, 20, "i = %d, j = %d"%(i,j), fontsize=5, rotation=0, color='y')
			#plt.text(0.1, 25, "ctr = %d"%(ctr), fontsize=5, rotation=0, color='y')
			
			
			p = plt.imshow(dispim,vmax = estimmax,vmin=0,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			
			
	
			ctr += 1
	
	
	
	plt.savefig(LOC+estim_plot%(pup,ff), dpi=150)
	plt.close()
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	for pup in PUPILS:
		for ff in FLAT_FIELD_ERROR:
			PlotOutput(pup,ff)
	
	print 'done'
	
	
				
		
if __name__ == "__main__":
	
	main()