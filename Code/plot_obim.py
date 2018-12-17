import math
from FigArray import FigArray
import numpy as np
import pylab as plt
from astropy.io import fits

LOC = '/Users/kstlaurent/NIRISS NRM/'
OBIM_FILE = 'Plots/obim_0%d.fits'#(NL,C)
BIN_IMAGE_FILE = 'Images/%s_OPD%d_ff%.2f_L%.2f_C%.2f_bin_image.fits'#(pup,OPD,ff,L,C)

PUPILS = ['CLEARP','MASK_NRM']
OP_PATH_DIFF = ['162','810']
ff = 0.00

LENGTH = [1,4]
CONTRAST = [5,2]
LABEL = ['OBJECT','SR = ']

STUFF_PLOT = 'Plots/ObIm.pdf'#(ob)

PWR = 0.15
CLP = 1


def clip_obj():
	
	obj1 = fits.getdata(LOC+'Objects/binobj_L1.0_C5.0.fits',memmap=False)
	obj1 = obj1[37:44,37:44]
	fits.PrimaryHDU(data=obj1).writeto(LOC+'Plots/obim_02.fits', clobber=True)
	
	obj2 = fits.getdata(LOC+'Objects/binobj_L4.0_C2.0.fits',memmap=False)
	obj2 = obj2[37:44,37:44]
	fits.PrimaryHDU(data=obj2).writeto(LOC+'Plots/obim_05.fits', clobber=True)
	
	obj3 = fits.getdata(LOC+'Images/MASK_NRM_OPD162_ff0.00_L1.00_C5.0_N1E+07_noisy_image.fits',memmap=False)
	#obj3 = obj3[37:44,37:44]
	fits.PrimaryHDU(data=obj3).writeto(LOC+'Plots/obim_01.fits', clobber=True)

	obj4 = fits.getdata(LOC+'Images/MASK_NRM_OPD162_ff0.00_L4.00_C2.0_N1E+07_noisy_image.fits',memmap=False)
	#obj4 = obj4[37:44,37:44]
	fits.PrimaryHDU(data=obj4).writeto(LOC+'Plots/obim_04.fits', clobber=True)
	
	obj5 = fits.getdata(LOC+'Images/CLEARP_OPD810_ff0.00_L1.00_C5.0_N1E+07_noisy_image.fits',memmap=False)
	#obj5 = obj5[37:44,37:44]
	fits.PrimaryHDU(data=obj5).writeto(LOC+'Plots/obim_00.fits', clobber=True)

	obj6 = fits.getdata(LOC+'Images/CLEARP_OPD810_ff0.00_L4.00_C2.0_N1E+07_noisy_image.fits',memmap=False)
	#obj6 = obj6[37:44,37:44]
	fits.PrimaryHDU(data=obj6).writeto(LOC+'Plots/obim_03.fits', clobber=True)
	
	
def get_stuff():
	
	files_list = []
	max_list = []
	for i in range(6):
		object = fits.getdata(LOC+OBIM_FILE%(i),memmap=False)
		files_list.append(object)
		max_list.append(object.max())
	
	return files_list,max_list
	
def PlotStuff():	
	files_list,max_list = get_stuff()
	
	x = 2
	y = 3
	
	INframeW = 1.5
	INframeH = 1.5
	INgapw = 0.05*np.ones(x+1)
	INgapw[0] = 0.2
	INgaph = 0.05*np.ones(y+1)
	INgaph[3] = 0.2
	INfig = FigArray(INframeW, INframeH, INgapw, INgaph)
	(W, H) = INfig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	plt.text(-0.08,1.085, "L = 1 pix, C = 5 mag", fontsize=10, rotation=0, color='k')
	plt.text(0.53,1.085, "L = 4 pix, C = 2 mag", fontsize=10, rotation=0, color='k')
	
	plt.text(-0.15,1.04, "detector scale model", fontsize=9, rotation=90, color='k')
	plt.text(-0.15,0.65, "NIRISS sim observation", fontsize=9, rotation=90, color='k')
	plt.text(-0.15,0.25, "NIRCam sim observation", fontsize=9, rotation=90, color='k')
	
	plt.axis('off')
	
	ctr = 0
	for i in range(0,x):
		for j in range(0,y):
			
			disp=files_list[ctr]
			disp = np.power(disp,PWR)
			#disp = disp_psf[30:55,30:55]
			
			dispmax = max_list[ctr]
			dispmax = np.power(dispmax,PWR)
			
			a = plt.axes(INfig.axes(i+1,j+1))
			
			#plt.text(0,1, '%d' %(ctr), fontsize=6, rotation=0, color='w')
			
			p = plt.imshow(disp,vmax=dispmax,vmin=0,cmap = 'hot',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1
			
	plt.savefig(LOC+STUFF_PLOT, dpi=150)

def main():
	#clip_obj()
	PlotStuff()

	
if __name__ == "__main__":
	main()

