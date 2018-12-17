import math
from FigArray import FigArray
import numpy as np
import pylab as plt
from astropy.io import fits

LOC = '/Users/kstlaurent/Box Sync/NIRISS NRM/'

BIN_IMAGE_FILE = 'Images/%s_OPD%s_ff%.2f_L%.2f_C%.2f_N%.0E_noisy_image.fits'#(pup,OPD,ff,L,C,phot)

IMAGE_PLOT = 'Documentation and Manuscripts/AGN with JWST II/IMAGES_CORE_L%d_C%d.eps'#(L,C)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""	
PUPILS = ['CLEARP','MASK_NRM']
OPD = '162'
fltr = 'F430M'
ff = 0.00
Nphotons = [1E4,1E7]

# L = 4.0, C = 1.0 ; L = 1.0, C = 5.0

PWR = 0.25
CLP = 1

def get_image(L,C):
	image_files = []
	image_max = []
	
	
	for phot in Nphotons:
		for pup in PUPILS:	
	
			image = fits.getdata(LOC+BIN_IMAGE_FILE%(pup,OPD,ff,L,C,phot),memmap=False)
			image_files.append(image)
			image_max.append(image.max())
	
	return image_files,image_max
				

def PlotIm(L,C):	
	image_files,image_max = get_image(L,C)
	
	x = len(Nphotons)
	y = len(PUPILS)
	
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
			
			image=image_files[ctr]
			imagemax = image_max[ctr]
			dispim = np.power(image,PWR)
			dispim = dispim[36:45,36:45]
			
			a = plt.axes(INfig.axes(i+1,j+1))
			
			plt.text(-0.3,0.5, "%s" %(PUPILS[j]), fontsize=5, rotation=0, color='y')
			plt.text(-0.3,-0.3, "Nphot = %.0E" %(Nphotons[i]), fontsize=5, rotation=0, color='y')
			
			p = plt.imshow(dispim,cmap = 'hot',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1
			
	plt.savefig(LOC+IMAGE_PLOT%(L,C), dpi=150)
	
	plt.close()

def main():
 	L1 = 4
 	C1 = 2
 		
 	L2 = 1
 	C2 = 5
 		
 	PlotIm(L1,C1)
 	PlotIm(L2,C2)
 		

if __name__ == "__main__":
	main()
