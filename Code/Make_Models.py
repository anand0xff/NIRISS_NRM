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


OBJECT_FILE = 'Objects/L%.1f_C%.1f_object.fits'#(NL,C)
BIN_IMAGE_FILE = 'Images/%s_OPD%d_ff%.2f_L%.2f_C%.1f_N%.0E_nonoise_image.fits'#(pup,OPD,ff,L,C,phot)
BIN_NOISY_IMAGE_FILE = 'Images/%s_OPD%d_ff%.2f_L%.2f_C%.1f_N%.0E_noisy_image.fits'#(pup,OPD,ff,L,C,phot)
SNR_FILE = 'SNR/%s_OPD%d_ff%.2f_L%.2f_C%.1f_SNR_bin_image.fits'#(Pup,OPD,ff,L,C)
OPD_FILE = 'OPD_RevV_niriss_%d.fits'#OPD


SUPPORT_FILE = 'Supports/L%.1f_support.fits'#(NL)
REF_OBJECT_FILE = 'Objects/L%.1f_C%.1f_ref.fits'#(NL,C)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""	
LENGTH = [1.0,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0,3.0,4.0,5.0]
PUPILS = ['MASK_NRM','CLEARP']
OP_PATH_DIFF = [162,810]
FLAT_FIELD_ERROR = [0.00,0.01,0.03]

ov = 11.00
fov = 81.00
narray = fov*ov
off = 0

M = 8.50
t = 1.00

Nphotons = [1E4,1E5,1E6,1E7]
fltr = 'F430M'
#filters_list =  ['F380M', 'F430M', 'F480M', 'F277W','CLEAR']

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
	
#point source, exactly 1 pixel in size
def ptsrc(M):
	object = np.zeros((M,M))
	object[M/2,M/2] = 1
	
	return object
	
def bar(L):
	
	object = np.zeros((narray,narray))
	xcenter = narray//2 - ov//2
	center = narray//2
	start = int(xcenter - L//2)
	stop = int(xcenter + L//2 + 1)
	if off == 0:
		intercept = center
	else:
		intercept = 0
	for i in range(start,stop):
		x = i
		y = off*x + intercept
		object[y,x] = 1
	return object
		
def webbpsf_maker(pup,OPD):
	ns = wp.NIRISS()
	SRC = 'A0V'
	src = poppy.specFromSpectralType(SRC)	
	ns.pupil_mask = pup
	ns.filter = fltr
	ns.pupilopd = LOC+'PSF/OPD_RevV_niriss_%d.fits'%OPD
	ns.calcPSF(outfile=LOC+PSF_FILE%(pup,OPD,fltr), source=src, fov_pixels=fov, oversample=ov, rebin=False, clobber=True)
	
def make_support(r):
	sup = r+1
	ctr = (fov/2,fov/2)
	pupil = makedisk(fov,ctr=ctr,radius=sup)			
	return pupil
	
def calc_SNR(a,b):
	signal = a
	noise = np.sqrt(b)	
	snr = signal/noise
	return snr

def perf_psf(pup):
	ns = wp.NIRISS()
	SRC = 'A0V'
	src = poppy.specFromSpectralType(SRC)	
	ns.pupil_mask = pup
	ns.filter = fltr
	ns.pupilopd = None
	ns.calcPSF(outfile=LOC+PERFECT_PSF%(pup,fltr), source=src, fov_pixels=fov, oversample=ov, rebin=False, clobber=True)

def OPD_maker():
	fits_obj = fits.open(LOC+'PSF/OPD_RevV_niriss_162.fits')
	new_OPD = 5*fits_obj[0].data
	fits_obj[0].data = new_OPD
	fits_obj.writeto(LOC+'PSF/OPD_RevV_niriss_810.fits', clobber=True)
	
def calc_strehl(pup,OPD):
	psf = fits.getdata(LOC+PSF_FILE%(pup,OPD,fltr))
	perf = fits.getdata(LOC+PERFECT_PSF%(pup,fltr))	
	return psf.max()/perf.max()
			
def rebin(a, bin_factor): 
	shape = a.shape[0]//bin_factor
	sh = shape,a.shape[0]//shape,shape,a.shape[1]//shape
	return a.reshape(sh).sum(-1).sum(1)
	
def dec_rebin(a,bin_factor):
	return a[::bin_factor,::bin_factor]

def reference_object(obj):
	ft = matrixDFT.MatrixFourierTransform()
	obj_transform = ft.perform(obj,narray,narray)
	
	cropped_obj_transform = np.zeros(narray*narray).reshape(narray,narray)
	cropped_obj_transform[439:450,439:450] = obj_transform[439:450,439:450]
	
	ref_obj = ft.inverse(cropped_obj_transform,narray,narray)
	detector_ref_obj = rebin(ref_obj,ov)
	
	return detector_ref_obj
		
def make_images(L,NL,C,pup,OPD,ff,phot):
	
	m = M + C
	nm = M + 0.5
	B = t*np.power(10.0,-M/2.5)
	b = (t*np.power(10.0,-m/2.5))/L
	nb = (t*np.power(10.0,-nm/2.5))/77
	flux_ratio = np.power(10.0,-C/2.5)
	
	#support = make_support(NL/2)
	#fits.PrimaryHDU(data=support).writeto(LOC+SUPPORT_FILE%(NL), clobber=True)
	
	psf = fits.getdata(LOC+PSF_FILE%(pup,OPD,fltr)) 
	bin_psf = rebin(psf,ov)*phot/(1+flux_ratio)
	fits.PrimaryHDU(data=bin_psf).writeto(LOC+BIN_PSF_FILE%(pup,OPD,fltr,phot,C), clobber=True)
				
	object = b*bar(L) + B*ptsrc(narray)
	fits.PrimaryHDU(data=object).writeto(LOC+OBJECT_FILE%(NL,C), clobber=True)	
				
	data = signal.fftconvolve(object,psf,mode='same')
	data = (data/data.sum())*phot
	
	if ff == 0:
		flatfielderror = 1
	else:
		flatfielderror = 1 + np.random.normal(loc = 0.0, scale = ff, size = (fov,fov))
	
	bin_data = rebin(data,ov)/flatfielderror
	fits.PrimaryHDU(data=bin_data).writeto(LOC+BIN_IMAGE_FILE%(pup,OPD,ff,NL,C,phot), clobber=True)
	
	noisy_data = np.random.poisson(data)
	bin_noisy_data = rebin(noisy_data,ov)/flatfielderror
	fits.PrimaryHDU(data=bin_noisy_data).writeto(LOC+BIN_NOISY_IMAGE_FILE%(pup,OPD,ff,NL,C,phot), clobber=True)
	
	bar_data = signal.fftconvolve(b*bar(L),psf,mode='same')
	bar_data = flux_ratio*phot*(bar_data/bar_data.sum())/(1+flux_ratio)
	bar_data = dec_rebin(bar_data,ov)
	
	#snr = calc_SNR(bar_data,bin_psf)			
	#fits.PrimaryHDU(data=snr).writeto(LOC+SNR_FILE%(pup,OPD,ff,NL,C), clobber=True)
	
	#detector_ref_obj = reference_object(object)
	#fits.PrimaryHDU(data=abs(detector_ref_obj)).writeto(LOC+REF_OBJECT_FILE%(NL,C), clobber=True)
	
	
					
def main():
	#OPD_maker()
	for pup in PUPILS:
		#perf_psf(pup)
		for OPD in OP_PATH_DIFF:
			for phot in Nphotons:
				#webbpsf_maker(pup,OPD)
				print OPD, 'psf done'
				#SR = calc_strehl(pup,OPD)
				#print OPD, '%.3f'%SR
				for ff in FLAT_FIELD_ERROR:
					for NL in LENGTH:
						L = NL*ov
						for C in CONTRAST:
							print pup,OPD,ff,NL,C
							make_images(L,NL,C,pup,OPD,ff,phot)
					
					
	
if __name__ == "__main__":
	main()
#	calc_strehl()
	
