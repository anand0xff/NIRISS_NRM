import math
from FigArray import FigArray
import numpy as np
import pylab as plt
from astropy.io import fits

LOC = '/Users/kstlaurent/NIRISS NRM/'
MASK_FILE = 'PSF/%s.fits'#(pup)
BIN_PSF_FILE = 'PSF/%s.%s.%s.bin_PSF.fits'#(pup,OPD,fltr)
PSF_FILE = 'PSF/%s.%s.%s.PSF.fits'#(pup,OPD,fltr)
PERFECT_PSF = 'PSF/Perfect.%s.%s.PSF.fits'#(pup,OPD,fltr)

PSF_PLOT = 'Plots/PSFs.pdf'#(ob)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""	
PUPILS = ['CLEARP','MASK_NRM']
OP_PATH_DIFF = ['MASK','162','810']
fltr = 'F430M'

PWR = 0.15
CLP = 1
	
def calc_strehl(pup,OPD):
	psf = fits.getdata(LOC+PSF_FILE%(pup,OPD,fltr))
	perf = fits.getdata(LOC+PERFECT_PSF%(pup,fltr))	
	return psf.max()/perf.max()

def get_psf():
	psf_files = []
	psf_max = []
	SR_list = []
		
	for pup in PUPILS:
		for OPD in OP_PATH_DIFF:
			psf = fits.getdata(LOC+BIN_PSF_FILE%(pup,OPD,fltr),memmap=False)[::-1,:]
			psf_files.append(psf)
			psf_max.append(psf.max())
			if OPD == 'MASK':
				sr = None
			else:
				sr = calc_strehl(pup,OPD)
			SR_list.append(sr)
	return psf_files,psf_max,SR_list
				

def PlotPSF():	
	psf_files,psf_max,SR_list = get_psf()
	
	x = len(PUPILS)
	y = len(OP_PATH_DIFF)
	
	INframeW = 1.5
	INframeH = 1.5
	INgapw = 0.05*np.ones(x+1)
	#INgapw[0] = 0.2
	INgaph = 0.05*np.ones(y+1)
	#INgaph[3] = 0.2
	INfig = FigArray(INframeW, INframeH, INgapw, INgaph)
	(W, H) = INfig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	ctr = 0
	for i in range(0,x):
		for j in range(0,y):
			
			psf=psf_files[ctr]
			psfmax = psf_max[ctr]
			SR = SR_list[ctr]
			psfmax = psfmax
			disp_psf = psf
			disp_psf = np.power(psf,PWR)
			#disp_psf = disp_psf[30:55,30:55]
			
			a = plt.axes(INfig.axes(i+1,y-j))
			
			if SR == None:
				plt.text(0,45, "%s" %(PUPILS[i]), fontsize=6, rotation=0, color='w')
			
			else:
				plt.text(0,7.5, "SR = %.2f" %(SR), fontsize=6, rotation=0, color='w')
				plt.text(0,3, "OPD = %s" %(OP_PATH_DIFF[j]), fontsize=6, rotation=0, color='w')
				
			p = plt.imshow(disp_psf,cmap = 'hot',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1
			
	plt.savefig(LOC+PSF_PLOT, dpi=150)
	
if __name__ == "__main__":
	PlotPSF()
