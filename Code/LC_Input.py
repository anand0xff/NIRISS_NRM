import math
from FigArray import FigArray
import numpy as np
import pylab as plt
from astropy.io import fits

LOC = '/Users/kstlaurent/Dropbox/NIRISS NRM/'

OBJECT_FILE = 'Objects/binobj_L%.1f_C%.1f.fits'#(NL,C)
BIN_IMAGE_FILE = 'Images/%s_OPD%d_ff%.2f_L%.2f_C%.2f_N%.0E_%s_image.fits'#(pup,OPD,ff,L,C,phot,noise)
SNR_FILE = 'SNR/%s_OPD%d_ff%.2f_L%.2f_C%.2f_SNR_bin_image.fits'#(Pup,OPD,ff,L,C)

OBJECT_PLOT= 'Plots/All_Objects.pdf'#(ob)
IMAGE_PLOT = 'Plots/%sImage_%s_OPD%d_ff%.2f_N%.0E.pdf'#(pup,OPD)
SNR_PLOT = 'Plots/SNR_%s_OPD%d_ff%.2f.pdf'#(ob,OPD)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""	
LENGTH = [1.0,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0,3.0,4.0,5.0]
PUPILS = ['MASK_NRM','CLEARP']
OP_PATH_DIFF = [162,810]
FLAT_FIELD_ERROR = [0.00,0.01,0.03]
Nphotons = [1E4,1E5,1E6,1E7]
NOISE = ['nonoise','noisy']

PWR = 0.25
CLP = 1
cap = 70000.0



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
plotting the inputted objects, the supports, the retrieved objects, and the residuals
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""								
def grab_input():
	
	objectfiles = []
	imagefiles = []
	SNRfiles = []
	
	ob_max = []
	image_max = []
	snr_max = []
	
	for NL in LENGTH:
		for C in CONTRAST:
			
			object = fits.getdata(LOC+OBJECT_FILE%(NL,C),memmap=False)
			objectfiles.append(object)
			ob_max.append(object.max())
			
			#image = fits.getdata(LOC+BIN_IMAGE_FILE%(pup,OPD,ff,NL,C,phot,no),memmap=False)
			#imagefiles.append(image)
			#image_max.append(image.max())
			
			#SNR = fits.getdata(LOC+SNR_FILE%(pup,OPD,ff,NL,C),memmap=False)
			#SNRfiles.append(SNR)
			#snr_max.append(SNR.max())
			
	return objectfiles,ob_max,imagefiles,image_max,SNRfiles,snr_max
	
def PlotInput():	
	objectfiles,ob_max,imagefiles,image_max,SNRfiles,snr_max = grab_input()
	
	x = len(LENGTH)
	y = len(CONTRAST)
	
	INframeW = 0.95
	INframeH = 0.95
	INgapw = 0.05*np.ones(x+1)
	INgaph = 0.05*np.ones(y+1)
	INfig = FigArray(INframeW, INframeH, INgapw, INgaph)
	(W, H) = INfig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	ctr = 0
	for i in range(0,x):
		for j in range(0,y):
			
			object=objectfiles[ctr]
			obmax = ob_max[ctr]
			obmax = np.power(obmax,PWR)
			dispobj = np.power(object,PWR)
			#dispobj = dispobj[410:479,410:479]
			dispobj = dispobj[37:44,37:44]
			
			a = plt.axes(INfig.axes(i+1,j+1))
			
			plt.text(-0.4,0.5, "L = %.2f pix" %(LENGTH[i]), fontsize=7, rotation=0, color='y')
			plt.text(-0.4,-0.3, "C = %.1f mag" %(CONTRAST[j]), fontsize=7, rotation=0, color='y')
			
			p = plt.imshow(dispobj,vmax=CLP*obmax,vmin=0,cmap = 'hot',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1
			
	plt.savefig(LOC+OBJECT_PLOT, dpi=150)

def main():
	PlotInput()
	print 'Done'
		
	
if __name__ == "__main__":
	main()