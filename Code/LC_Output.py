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

LOC = '/Users/kstlaurent/Documents/NIRISS NRM/'

ESTIM_FILE = 'Estim/%s_OPD%d_ff%.2f_L%.2f_C%.1f_N%.0E_%s_estim.fits'#(pup,OPD,ff,NL,C,phot,no,i,j)
SUPPORT_FILE = 'Supports/L4.0_support.fits'#(NL)
OBJECT_FILE = 'Objects/L%.1f_C%.1f_object.fits'#(NL,C)
BIN_OBJECT = 'Objects/binobj_L%.1f_C%.1f.fits'#(NL,C)
estim_plot = 'Plots/%sEstim_%s_%d_%d_N%d.pdf'#(no,pup,obd,ff,phot)

LENGTH = [1.0,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0,3.0,4.0,5.0]
PUPILS = ['CLEARP','MASK_NRM']
OP_PATH_DIFF = [162,810]
FLAT_FIELD_ERROR = [0.00,0.03]
Nphotons = [1E7]
NOISE = ['noisy']

PWR = 0.25
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
def grab_files(pup,opd,ff,phot,no):

	estimlist = []
	estimmaxlist = []
	estimminlist = []
	metricnumlist = []
	
	for NL in LENGTH:
		for C in CONTRAST:
		
	
			
			estim = fits.getdata(LOC+ESTIM_FILE%(pup,opd,ff,NL,C,phot,no))
			estimlist.append(estim)
			estimmaxlist.append(estim.max())
			estimminlist.append(estim.min())
			
			real_obj = calc_real(NL,C)
			support = fits.getdata(LOC+SUPPORT_FILE)
			
			metricnum = calc_metric(estim,real_obj,1,phot,support)
			metricnumlist.append(metricnum)
			
	return estimlist, estimmaxlist,estimminlist, metricnumlist
	
def PlotOutput(pup,opd,ff,phot,no):
	
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
	
	estimlist, estimmaxlist,estimminlist,metricnumlist = grab_files(pup,opd,ff,phot,no)

	plt.axis("off")

	ctr = 0
	for i in range(x):
		for j in range(y):
			
			dispim = np.power(estimlist[ctr],PWR)
			dispim = dispim[37:44,37:44]
			
			estimmax = np.power(estimmaxlist[ctr],PWR)
	
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,j+1))
		
			#plt.text(0.1,6, "length = %.2f" %(LENGTH[i]), fontsize=5, rotation=0, color='w')
			#plt.text(0.1,13, "C = %.1f" %(CONTRAST[j]), fontsize=5, rotation=0, color='w')
			#plt.text(0,9, "M = %.2E"%(metricnumlist[ctr]), fontsize=5, rotation=0, color='w')
			p = plt.imshow(dispim,vmax = estimmax,vmin=0,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1

	plt.savefig(LOC+estim_plot%(no,pup,opd,ff*100,np.log10(phot)), dpi=150)
	plt.close()
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	for no in NOISE:
		for pup in PUPILS:
			for opd in OP_PATH_DIFF:
				for ff in FLAT_FIELD_ERROR:
					for phot in Nphotons:		
						PlotOutput(pup,opd,ff,phot,no)
						print no,pup,opd,ff,'%.0E'%phot,'done'
				
		
if __name__ == "__main__":
	
	main()