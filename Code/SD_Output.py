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

LOC = '/Users/kstlaurent/Box Sync/NRM/Work/NIRISS NRM/'

object_file = 'Objects/%s/%s/L%.2f_C%.1f_bin_object.fits'#(ob,offset,NL,C)
estim_file = 'L1L2space/%s/%s/noisy_estim/E_%s_L%.2f_C%.1f_s%02dd%02d.fits'#(ob,off,pup,NL,C,scales[i],deltas[j])
resid_file = 'L1L2space/%s/%s/noisy_resid/R_%s_L%.2f_C%.1f_s%02dd%02d.fits'#(ob,off,pup,NL,C,scales[i],deltas[j])


estim_plot = 'Plots/SD output/noisy_estim/E_%s_%s_%s_L%.1f_C%.1f.pdf'#(pup,ob,off,NL,C)
resid_plot = 'Plots/SD output/noisy_resid/R_%s_%s_%s_L%.1f_C%.1f_R.pdf'#(pup,ob,off,NL,C)

LENGTH = [0.25,0.50,1.00,1.50,2.00]
CONTRAST = [2.0,3.0,4.0,5.0,6.0]
PUPILS = ['MASK_NRM','CLEARP']
offset = ['no_offset','offset']
object = ['Bar','Bar+Point']

Nphotons = 1E8
scales = [3.16,10,31.6,100,316]
deltas = [0.30,0.60,1.00,1.50,2.00]
N = len(scales)

PWR = 0.25
CLP = 0.7

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
calculates the residuals, based on the true object. flux is normalized such that the 
brightest pixel is one. 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def calc_res(ob,off,pup,NL,C):
	
	for i in range(0,N):
		for j in range(0,N):
			
			estim = fits.getdata(LOC+estim_file%(ob,off,pup,NL,C,i,j),memmap=False)
			estim = estim/estim.max()
			
			sky = fits.getdata(LOC+object_file%(ob,off,NL,C), memmap=False)
			sky = sky/sky.max()

			resid =  sky - estim	
			abs_resid = abs(resid)
					
			fits.PrimaryHDU(data=abs_resid).writeto(LOC+resid_file%(ob,off,pup,NL,C,i,j), clobber=True)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
plotting the retrieved objects and the residuals
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def grab_files(ob,off,pup,NL,C):

	estimfiles = []
	residfiles = []
	estimmaxlist = []
	residmaxlist = []
	for i in range(N):
		for j in range(N):
			
			estimfiles.append(fits.getdata(LOC+estim_file%(ob,off,pup,NL,C,i,j),memmap=False))
			residfiles.append(fits.getdata(LOC+resid_file%(ob,off,pup,NL,C,i,j),memmap=False))
			
			estimmaxlist.append(np.nanmax(estimfiles))
			residmaxlist.append(np.nanmax(residfiles))
			
	return estimfiles,estimmaxlist,residfiles,residmaxlist
	
def PlotOutput(ob,off,pup,NL,C):
	
	frameW = 0.95
	frameH = 0.95
	gapw = 0.05*np.ones(N+1)
	gaph = 0.05*np.ones(N+1)
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	estimfiles,estimmaxlist,residfiles,residmaxlist = grab_files(ob,off,pup,NL,C)

	ctr = 0
	
	for i in range(N):
		for j in range(N):
			
			dispim = np.power(estimfiles[ctr],PWR)
			dispim = dispim[35:45,35:45]
			
			estimmax = np.power(estimmaxlist[ctr],PWR)

			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,N - j))
		
			#values of SCALES and DELTAS
			plt.text(0,1, "$s = %.2E}$" %(scales[i]), fontsize=6, rotation=0, color='w')
			plt.text(0, 0, "$d = %.2f$" %(deltas[j]), fontsize=6, rotation=0, color='w')
			
			p = plt.imshow(dispim,vmax = CLP*estimmax,vmin=0,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1

	plt.savefig(LOC+estim_plot%(pup,ob,off,NL,C), dpi=150)

	ctr = 0
	
	for i in range(N):
		for j in range(N):
			
			dispim = residfiles[ctr]
			dispim = dispim[35:45,35:45]
			
			residmax = residmaxlist[ctr]
			
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,N - j))
			
			#values of SCALES and DELTAS
			plt.text(0,1, "$s = %.2E}$" %(scales[i]), fontsize=6, rotation=0, color='w')
			plt.text(0, 0, "$d = %.2f$" %(deltas[j]), fontsize=6, rotation=0, color='w')
			
			p = plt.imshow(dispim,vmax = residmax,vmin = 0,cmap = 'gist_heat',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1

	plt.savefig(LOC+resid_plot%(pup,ob,off,NL,C), dpi=150)
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	for ob in object:
		for off in offset:
			for pup in PUPILS:
				for NL in LENGTH:
					for C in CONTRAST:		
						calc_res(ob,off,pup,NL,C)
						print ob,off,pup,NL,C, 'plotting...'		
						PlotOutput(ob,off,pup,NL,C)
						print ob,off,pup,NL,C,'done'
				
		
if __name__ == "__main__":
	
	main()