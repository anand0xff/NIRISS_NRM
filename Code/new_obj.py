import sys, os, time
import numpy as np
import scipy.special
from scipy import signal
from scipy import stats
from astropy.io import fits
import math
import gc
import string
from datetime import datetime
import matrixDFT

LOC = '/Users/kstlaurent/Box Sync/NIRISS NRM/'

BIN_IMAGE_FILE = 'Images/%s_OPD%d_ff%.2f_L%.2f_C%.2f_bin_image.fits'#(pup,OPD,ff,L,C)
BIN_PSF_FILE = 'PSF/%s.%d.%s.bin_PSF.fits'#(pup,OPD,fltr)
NEW_OBJECT_FILE = 'New Object/%s_OPD%d_ff%.2f_L%.2f_C%.2f.fits'#(pup,OPD,ff,L,C)'
NEW_REAL_OBJECT_FILE = 'New Real/real_%s_OPD%d_ff%.2f_L%.2f_C%.2f.fits'#(pup,OPD,ff,L,C)'
NEW_IMAG_OBJECT_FILE = 'New Imag/imag_%s_OPD%d_ff%.2f_L%.2f_C%.2f.fits'#(pup,OPD,ff,L,C)'

PUPILS = ['CLEARP','MASK_NRM']
OP_PATH_DIFF = [162]#,810]
FLAT_FIELD_ERROR = [0.00]
LENGTH = [4.0]
CONTRAST = [2.0]

fltr = 'F430M'

def check_object(a,b,thresh_percent,pup,opd,ff,NL,C):
	ft = matrixDFT.MatrixFourierTransform()
	
	narray = a.shape[0]
	
	CV = ft.perform(a,narray,narray)
	OTF = ft.perform(b,narray,narray)
	
	thresh = abs(OTF).max()*thresh_percent
	idx = np.where(abs(OTF)>=thresh)
	
	objtfm = np.zeros(narray*narray).reshape(narray,narray)
	
	objtfm[idx] = CV[idx]/OTF[idx]
	
	ant_alias = makedisk(narray,ctr = (40,40),radius = 20)
	
	new_obj = ft.inverse(objtfm*ant_alias,narray,narray)
	
	return new_obj, CV

def check_complex(a):
	real_sum = a.real.sum()
	imag_sum = a.imag.sum()
	
	complex_ratio = imag_sum/real_sum
	
	return real_sum, imag_sum, complex_ratio
	
def makedisk(s, ctr=None, radius=None):
	return make_ellipse(s, ctr=ctr, ellpars = (radius,radius,0.0))
	
def make_ellipse(s, ctr=None, ellpars = None):
	ss = (s,s)
	# choose a pixel-centric center default for odd-sizes, pixelcornercentric for even
	if ctr is None:
		ctr = (ss[0]/2.0, ss[1]/2.0)	
	xx = np.linspace(-ctr[0]+0.5, ss[0]-ctr[0]-0.5, ss[0]) 	
	yy = np.linspace(-ctr[1]+0.5, ss[1]-ctr[1]-0.5, ss[1])
	(x,y) = np.meshgrid(xx, yy.T)	
	deg = -np.pi/180.0
	semimajor, semiminor, theta = ellpars
	esq = (x*np.cos(theta/deg) - y*np.sin(theta/deg))**2 / semimajor**2 + \
	      (y*np.cos(theta/deg) + x*np.sin(theta/deg))**2 / semiminor**2
	array = np.zeros(ss)
	array[esq<1] = 1
	return array
		

def main():
	for pup in PUPILS:
		for opd in OP_PATH_DIFF:
			for ff in FLAT_FIELD_ERROR:
				for NL in LENGTH:
					for C in CONTRAST:
						data = fits.getdata(LOC+BIN_IMAGE_FILE%(pup,opd,ff,NL,C))
						psf = fits.getdata(LOC+BIN_PSF_FILE%((pup,opd,fltr)))
						
						thresh_percent = .001
						
						obj,cv = check_object(data,psf,thresh_percent,pup,opd,ff,NL,C)
						
						fits.PrimaryHDU(data=obj.real).writeto(LOC+NEW_REAL_OBJECT_FILE%(pup,opd,ff,NL,C), clobber=True)
						fits.PrimaryHDU(data=obj.imag).writeto(LOC+NEW_IMAG_OBJECT_FILE%(pup,opd,ff,NL,C), clobber=True)
						
						fits.PrimaryHDU(data=cv.real).writeto(LOC+'cv_real_%s.fits'%(pup), clobber=True)
						fits.PrimaryHDU(data=cv.imag).writeto(LOC+'cv_imag_%s.fits'%(pup), clobber=True)
						real_sum, imag_sum, complex_ratio = check_complex(obj)
						
						print pup, opd,ff,NL,C, '%.2E'%real_sum, '%.2E'%imag_sum, '%.2E'%complex_ratio
						
						whole_obj = abs(obj)
						
						fits.PrimaryHDU(data=whole_obj).writeto(LOC+NEW_OBJECT_FILE%(pup,opd,ff,NL,C), clobber=True)
						

if __name__ == "__main__":
	main()