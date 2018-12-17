from astropy.io import fits
import numpy as np
import sys, os
import math
from scipy import signal
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import *
from pylab import *

LOC = '/Users/kstlaurent/Box Sync/NRM/Work/NIRISS NRM/'
BIN_PSF_FILE = 'PSF/%s.%s.bin_PSF.fits'#(pup,fltr)
BIN_IMAGE_FILE = 'Images/%s/%s/%s_L%.2f_C%.1f_bin_noisy_image.fits'#(ob,off,Pup,L,C)
NOISY_BIN_IMAGE_FILE = 'Images/%s/%s/%s_L%.2f_C%.1f_bin_noisy_image.fits'#(ob,off,pup,L,C)
SNR_FILE = 'SNR/%s/%s/%s_L%.2f_C%.1f_SNR_bin_image.fits'#(ob,off,Pup,L,C)
NOISY_SNR_FILE = 'SNR/%s/%s/%s_L%.2f_C%.1f_SNR_bin_noisy_image.fits'#(ob,offPup,L,C)

ov = 11.00
fov = 81.00
narray = fov*ov

fltr = 'F430M'
Nphotons = 1E8

M = 8.50
t = 1.00
PUPILS = ['MASK_NRM','CLEARP']
LENGTH = [0.50,1.00,2.00,3.00]
CONTRAST = [3.0,4.0,5.0,6.0]
offset = ['no_offset','offset']
object = ['Bar','Bar+Point']
N = len(LENGTH)

def calc_SNR(data,psf):

	signal = data 
	noise = np.sqrt(psf)	
	snr = signal/noise
	
	return snr

def main():
	for ob in object:
		for off in offset:
			for pup in PUPILS:
				for i in range(N):
					for j in range(N):
						
						psf = fits.getdata(LOC+BIN_PSF_FILE%(pup,fltr))
						
						bin_data = fits.getdata(LOC+BIN_IMAGE_FILE%(ob,off,pup,LENGTH[i],CONTRAST[j]))
						bin_noisy_data = fits.getdata(LOC+NOISY_BIN_IMAGE_FILE%(ob,off,pup,LENGTH[i],CONTRAST[j]))	
						
						
						snr = calc_SNR(bin_data,psf,CONTRAST[j])
						noisy_snr = calc_SNR(bin_noisy_data,psf,CONTRAST[j])
				
						fits.PrimaryHDU(data=snr).writeto(LOC+SNR_FILE%(ob,off,pup,LENGTH[i],CONTRAST[j]), clobber=True)
						fits.PrimaryHDU(data=noisy_snr).writeto(LOC+NOISY_SNR_FILE%(ob,off,pup,LENGTH[i],CONTRAST[j]), clobber=True)
						print ob, off, pup, i,j

if __name__ == "__main__":
	main()
	