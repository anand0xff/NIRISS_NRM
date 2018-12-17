import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import *
from pylab import *
from astropy.io import fits
import numpy as np
from FigArray import FigArray


LOC = '/Users/kstlaurent/Box Sync/NRM/Work/NIRISS NRM/'
SNR_FILE = 'SNR/%s/%s/%s_L%.2f_C%.1f_SNR_bin_image.fits'#(offset,Pup,L,C)

SNR_PLOT = 'Plots/Input/%s_%s_%s_BinImage_SNR.pdf'#(pup,offset)

LENGTH = [0.50,1.00,2.00,3.00]
CONTRAST = [3.0,4.0,5.0,6.0]
object = ['Bar','Bar+Point']

x = len(LENGTH)
y = len(CONTRAST)

PWR = 0.25

PUPILS = ['MASK_NRM','CLEARP']
offset = ['no_offset','offset']

def grab_files(ob,pup,off):
	SNR_files = []
	
	for NL in LENGTH:
		for C in CONTRAST:	
			SNR_files.append(fits.getdata(LOC+SNR_FILE%(ob,off,pup,NL,C),memmap=False))	
			
	return SNR_files	

def plot_SNR(ob,pup,off):
	
	SNR_files = grab_files(ob,pup,off)
	
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
			
			SNR = SNR_files[ctr]
			
			dispim = np.power(SNR,PWR)
			dispim = dispim[20:61,20:61]
			print '%.2E'%dispim.max(),'%.2E'%dispim.min()
			
			a = plt.axes(INfig.axes(i+1,j+1))
			
			plt.text(0,4, "L = %.2f NIRISS Pixels" %(LENGTH[i]), fontsize=6, rotation=0, color='y')
			plt.text(0,0, "C = %.1f mag" %(CONTRAST[j]), fontsize=6, rotation=0, color='y')
			p = plt.imshow(dispim,vmax=3,vmin=0, cmap = 'hot',interpolation='nearest')
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			plt.axis("off")
			
			ctr += 1
			
	plt.savefig(LOC+SNR_PLOT%(pup,ob,off), dpi=150)


def main():
	for ob in object:
		for off in offset:
			for pup in PUPILS:
				print ob,off, pup
				plot_SNR(ob,pup,off)
			

if __name__ == "__main__":
	main()
