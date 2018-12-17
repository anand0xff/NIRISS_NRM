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
MODEL_FILE = 'realer_objects/ARP_085_I_IRAC_4.5_ssh2007.fits'
OBJECT_FILE = 'realer_objects/cropped_padded_ARP_085_I_IRAC_4.5_ssh2007.fits'
BIN_OBJECT_FILE = 'realer_objects/ARP_085_I_IRAC_4.5_ssh2007_detector_scale.fits'

BIN_IMAGE_FILE = 'realer_images/%s_OPD%d_ff%.2f_%s_realer_N%.0E_image.fits'#(pup,OPD,ff,fltr,phot)
BIN_NOISY_IMAGE_FILE = 'realer_images/%s_OPD%d_ff%.2f_%s_realer_N%.0E_noisy_image.fits'#(pup,OPD,ff,fltr,phot)
OPD_FILE = 'OPD_RevV_niriss_%d.fits'#OPD


SUPPORT_FILE = 'Supports/L%.1f_support.fits'#(NL)
REF_OBJECT_FILE = 'Objects/L%.1f_C%.1f_ref.fits'#(NL,C)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""	
pup = 'MASK_NRM'
OPD = 162
FLAT_FIELD_ERROR = [0.00,0.03]

ov = 11.00
fov = 81.00
narray = fov*ov

Nphotons = [1E7,1E8]
fltr = 'F430M'
con = 0	
#filters_list =  ['F380M', 'F480M']

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
	
def reference_object(obj):
	ft = matrixDFT.MatrixFourierTransform()
	obj_transform = ft.perform(obj,narray,narray)
	
	cropped_obj_transform = np.zeros(narray*narray).reshape(narray,narray)
	cropped_obj_transform[439:450,439:450] = obj_transform[439:450,439:450]
	
	ref_obj = ft.inverse(cropped_obj_transform,narray,narray)
	detector_ref_obj = rebin(ref_obj,ov)
	
	return detector_ref_obj
		
def make_images(object,pup,ff,fltr,phot):
	
	C = con
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
	fits.PrimaryHDU(data=bin_data).writeto(LOC+BIN_IMAGE_FILE%(pup,OPD,ff,fltr,phot), clobber=True)
	
	noisy_data = np.random.poisson(lam=data,size=None)
	#bin_noisy_data = rebin(noisy_data,ov)/flatfielderror
	#fits.PrimaryHDU(data=bin_noisy_data).writeto(LOC+BIN_NOISY_IMAGE_FILE%(pup,OPD,ff,fltr,phot), clobber=True)	
					
def main():
	
	
	#webbpsf_maker(fltr)
			
	object = fits.getdata(LOC+MODEL_FILE)[216:940,109:833]
			
	padding_array = np.zeros(891*891).reshape(891,891)
			
	padding_array[83:807,83:807] = object
	
	padding_array[784,152] = 0.0
	
	total_flux = np.sum(padding_array)	
	
	if con == 0:
		padding_array[444,444] = padding_array[444,444]
	
	else:
		padding_array[444,444] = con*total_flux
	
	fits.PrimaryHDU(data=padding_array).writeto(LOC+OBJECT_FILE, clobber=True)
	
	print np.shape(padding_array)
	
	bin_ob = rebin(padding_array,ov)
	fits.PrimaryHDU(data=bin_ob).writeto(LOC+BIN_OBJECT_FILE, clobber=True)
	
	for phot in Nphotons:
		for ff in FLAT_FIELD_ERROR:
			print pup,phot,ff
			make_images(padding_array,pup,ff,fltr,phot)
					
					
	
if __name__ == "__main__":
	main()
	
