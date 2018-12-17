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

ESTIM_FILE = 'N1068_Ob/N1068_bar%.1f_ovsampx11_clipped_to_PSF_dim.fits'#(pup,ff,phot)


estim_plot = 'N1068_Plots/N1068_11xovsamp.pdf'#(pup,ff,phot)

PUPILS = ['MASK_NRM']
BAR_BRIGHTNESS = [0.0,0.3,1.0]
Nphotons = [1E8]
CAPTION = ['no bar','30% ring brightness','equal brightness']

PWR = 0.15
CLP = .8
ov = 11
fov = 81

#scales = [3.16,10,31.6,100,316]
#deltas = [0.30,0.60,1.00,1.50,2.00]

def calc_metric(a,b,k,phot,support=None):
	if support is None:
		support = np.ones(a.shape)
	
	supportidx = np.where(support==1)		
	metric = np.power(abs(a-b),k)/np.power(phot,k)
	return metric.sum()/len(supportidx[0])

def calc_real(NL,C):
	object = fits.getdata(LOC+OBJECT_FILE%(NL,C))
	bin_obj = rebin(object,ov)
	fits.PrimaryHDU(data=bin_obj).writeto(LOC+BIN_OBJECT%(NL,C), clobber=True)
	return rebin(object,ov)

def rebin(a, bin_factor): 
	shape = a.shape[0]//bin_factor
	sh = shape,a.shape[0]//shape,shape,a.shape[1]//shape
	return a.reshape(sh).sum(-1).sum(1)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
plotting the metric 'map'
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def grab_files():
	
	estimlist = []
	estimmaxlist = []
	estimminlist = []
	
	
	for bright in BAR_BRIGHTNESS:
		estim = fits.getdata(LOC+ESTIM_FILE%(bright))[::-1,:]
	
		print ESTIM_FILE%(bright)
	
		estimlist.append(estim)
		estimmaxlist.append(estim.max())
		estimminlist.append(estim.min())
			
	return estimlist, estimmaxlist,estimminlist
def PlotOutput():
	
	x = len(BAR_BRIGHTNESS)
	y = len(Nphotons)
	
	frameW = 1.5
	frameH = 1.5
	gapw = 0.05*np.ones(x+1)
	#gapw[0] = 0.4
	gaph = 0.05*np.ones(y+1)
	#gaph[2] = 0.4
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	estimlist, estimmaxlist,estimminlist = grab_files()

	ctr = 0
	
	#plt.text(1,1, "No bar", fontsize=5, rotation=0, color='b')
	#plt.text(0.55,1, "Bar brightness = 30% outer ring", fontsize=5, rotation=0, color='k')
	#plt.text(0.55,2, "Bar brightness = 30% outer ring", fontsize=5, rotation=0, color='k')
	#plt.text(-0.05,0.65, "Nphotons = 1E08", fontsize=5, rotation=90, color='k')
	#plt.text(-0.05,0.09, "Nphotons = 1E07", fontsize=5, rotation=90, color='k')
	plt.axis("off")
	
	
	for i in range(x):
		for j in range(y):
			
			dispim = np.power(estimlist[ctr],PWR)
			dispim = dispim[345:490,375:520]
			#145
			
			
			estimmax = np.power(322.5,PWR)
	
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,j+1))
		
			plt.text(0.1,6, "%s" %(CAPTION[i]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1,13, "%.0E" %(Nphotons[j]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1, 20, "i = %d, j = %d"%(i,j), fontsize=5, rotation=0, color='y')
			#plt.text(0.1, 25, "ctr = %d"%(ctr), fontsize=5, rotation=0, color='y')
			
			
			p = plt.imshow(dispim,vmax = estimmax,vmin=0,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			
			
	
			ctr += 1
	
	
	
	plt.savefig(LOC+estim_plot, dpi=150)
	plt.close()
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	PlotOutput()
	print 'done'
	
	
				
		
if __name__ == "__main__":
	
	main()