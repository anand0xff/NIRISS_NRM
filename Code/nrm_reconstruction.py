import sys, os, time
import numpy as np
import scipy.special
from scipy import signal
from scipy import stats
from astropy.io import fits
import math
import matrixDFT
from scipy import fftpack

LOC = '/Users/kstlaurent/Box Sync/NIRISS NRM/'
IMAGE_FILE = 'Images/wave_exp/%s_OPD%d_ff%.2f_L%.2f_C%.2f_bin_image.fits'#(pup,OPD,ff,NL,C)
BIN_PSF_FILE = 'PSF/%s.%d.%s.bin_PSF.fits'#(pup,OPD,fltr)
NEW_OBJECT_FILE = 'New Objects/%s_OPD%d_ff%.2f_L%.2f_C%.2f_newobject.fits'#(pup,OPD,ff,NL,C)

LENGTH = [1.0]#,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0]#,3.0,4.0,5.0]
PUPILS = ['MASK_NRM']#,'CLEARP']
OP_PATH_DIFF = [162]#,810]
FLAT_FIELD_ERROR = [0.00]#,0.01,0.03]
fltr = 'F430M'

ov = 11.00
fov = 81.00
narray = fov*ov
off = 0

M = 8.50
t = 1.00
B = t*np.power(10.0,-M/2.5)



def deconvolve(star, psf):
    
    
    
def main():
	for pup in PUPILS:
		for OPD in OP_PATH_DIFF:
			psf = fits.getdata(LOC+BIN_PSF_FILE%(pup,OPD,fltr))
			for NL in LENGTH:
				for C in CONTRAST:
					
					image = fits.getdata(LOC+IMAGE_FILE%(pup,OPD,ff,NL,C))		
					image_deconv = deconvolve(star_conv, psf)
					fits.PrimaryHDU(data=image_deconv).writeto(LOC+NEW_OBJECT_FILE%(pup,OPD,ff,NL,C), clobber=True)
						

if __name__ == "__main__":
	main()