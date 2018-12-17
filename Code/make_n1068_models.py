import sys, os, time
import numpy as np
import scipy.special
from scipy import signal
from scipy import stats
from astropy.io import fits
import math
from FigArray import FigArray
import gc
import string
from datetime import datetime
#import poppy
#import webbpsf as wp
import matrixDFT

LOC = '/Users/kstlaurent/NIRISS NRM/'

PSF_FILE = 'PSF/%s.%d.%s.PSF.fits'#(pup,OPD,fltr)
PERFECT_PSF = 'PSF/Perfect.%s.%s.PSF.fits'#(pup,OPD,fltr)
BIN_PSF_FILE = 'PSF/%s.%d.%s.%.0E.%.1f_bin_PSF.fits'#(pup,OPD,fltr,phot,C)

#add fltr keyword to file names
MODEL_FILE = 'N1068_Ob/test_segline_b1.fits'
OBJECT_FILE = 'N1068_Ob/N1068_bar%.1f_ovsampx11_clipped_to_PSF_dim.fits'
BIN_OBJECT_FILE = 'N1068_Ob/N1068_bar%.1f_detector_scale.fits'
BIN_NOISY_IMAGE_FILE = 'N1068_Im/%s_OPD%d_ff%.2f_%s_N1068_N%.0E_noisy_bar%.1f_image.fits'#(pup,OPD,ff,fltr,phot,bright)
OPD_FILE = 'OPD_RevV_niriss_%d.fits'#OPD


SUPPORT_FILE = 'Supports/L%.1f_support.fits'#(NL)
REF_OBJECT_FILE = 'Objects/L%.1f_C%.1f_ref.fits'#(NL,C)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""	
PUPILS = ['MASK_NRM','CLEARP']
OPD = 162
FLAT_FIELD_ERROR = [0.00,0.01]
bar_brightness = [1.0,0.3,0.0]
#offset = [0.0,1.0]

ov = 11.00
fov = 81.00
narray = fov*ov

Nphotons = [1E7,1E8]
#fltr = 'F430M'
filters_list =  ['F430M']

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""					
def rebin(a, bin_factor): 
	shape = a.shape[0]//bin_factor
	sh = shape,a.shape[0]//shape,shape,a.shape[1]//shape
	return a.reshape(sh).sum(-1).sum(1)
	
def dec_rebin(a,bin_factor):
	return a[::bin_factor,::bin_factor]
	
def webbpsf_maker(fltr):
	ns = wp.NIRISS()
	SRC = 'A0V'
	src = poppy.specFromSpectralType(SRC)	
	ns.pupil_mask = pup
	ns.filter = fltr
	ns.pupilopd = LOC+'PSF/OPD_RevV_niriss_%d.fits'%OPD
	ns.calcPSF(outfile=LOC+PSF_FILE%(pup,OPD,fltr), source=src, fov_pixels=fov, oversample=ov, rebin=False, clobber=True)
	
def bar(L,bright):
	
	object = np.zeros((narray,narray))
	xcenter = narray//2
	center = narray//2
	start = int(xcenter)
	stop = int(xcenter + L)
	
	off = 1
	
	if off == 0:
		intercept = center
	else:
		intercept = 0
	
	for i in range(start,stop):
		x = i  
		y = off*x + intercept
		object[y,x] = bright
	return object

def reference_object(obj):
	ft = matrixDFT.MatrixFourierTransform()
	obj_transform = ft.perform(obj,narray,narray)
	
	cropped_obj_transform = np.zeros(narray*narray).reshape(narray,narray)
	cropped_obj_transform[439:450,439:450] = obj_transform[439:450,439:450]
	
	ref_obj = ft.inverse(cropped_obj_transform,narray,narray)
	detector_ref_obj = rebin(ref_obj,ov)
	
	return detector_ref_obj
		
def make_images(object,pup,ff,fltr,phot,bright):
	
	C = 1.00
	flux_ratio = np.power(10.0,-C/2.5)
	
	psf = fits.getdata(LOC+PSF_FILE%(pup,OPD,fltr)) 
	bin_psf = rebin(psf,ov)*phot/(1+flux_ratio)
	fits.PrimaryHDU(data=bin_psf).writeto(LOC+BIN_PSF_FILE%(pup,OPD,fltr,phot,C), clobber=True)
							
	data = signal.fftconvolve(object,psf,mode='same')
	data = (data/data.sum())*phot
	
	if ff == 0:
		flatfielderror = 1
	else:
		flatfielderror = 1 + np.random.normal(loc = 0.0, scale = ff, size = (fov,fov))
	
	bin_data = rebin(data,ov)/flatfielderror
	#fits.PrimaryHDU(data=bin_data).writeto(LOC+BIN_IMAGE_FILE%(pup,OPD,ff,NL,C,phot), clobber=True)
	
	noisy_data = np.random.poisson(data)
	bin_noisy_data = rebin(noisy_data,ov)/flatfielderror
	fits.PrimaryHDU(data=bin_noisy_data).writeto(LOC+BIN_NOISY_IMAGE_FILE%(pup,OPD,ff,fltr,phot,bright), clobber=True)	
					
def main():
	
	for pup in PUPILS:	
		for bright in bar_brightness:
			for fltr in filters_list:
			
				#webbpsf_maker(fltr)
			
				object = fits.getdata(LOC+MODEL_FILE)[259:1150,259:1150]
		
				object = object + bar(28,bright)
		
				fits.PrimaryHDU(data=object).writeto(LOC+OBJECT_FILE%bright, clobber=True)
	
				bin_ob = rebin(object,ov)
				fits.PrimaryHDU(data=bin_ob).writeto(LOC+BIN_OBJECT_FILE%bright, clobber=True)
	
				for phot in Nphotons:
					for ff in FLAT_FIELD_ERROR:
						print bright,pup,phot,ff
						make_images(object,pup,ff,fltr,phot,bright)
					
					
	
if __name__ == "__main__":
	main()
	
