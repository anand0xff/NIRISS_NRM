import sys, os
from FigArray import FigArray
import numpy as np
import pylab as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from PIL import Image, ImageFilter

from mpl_toolkits.mplot3d import Axes3D

LOC = '/Users/kstlaurent/NIRISS NRM/'

estim_plot = 'Plots/NoisyEstimBars_%s_ff%.2f_N1E+07.jpg'#(pup,ff)
figure = 'Plots/Estim.pdf'#(pup,ff,phot)

PUPILS = ['MASK_NRM','CLEARP']
FLAT_FIELD_ERROR = [0.00,0.03]

PWR = 0.15
CLP = .8
ov = 11
fov = 81


def grab_files():
	
	estimlist = []
	estimmaxlist = []
	estimminlist = []
	
	
	for pup in PUPILS:
		for ff in FLAT_FIELD_ERROR:
				estim = Image.open(LOC+estim_plot%(pup,ff))
				estimlist.append(estim)
		
	return estimlist
	
def PlotOutput():
	
	x = len(PUPILS)
	y = len(FLAT_FIELD_ERROR)
	
	frameW = 1.5
	frameH = 1
	gapw = 0.1*np.ones(x+1)
	#gapw[0] = 0.2
	gaph = 0.1*np.ones(y+1)
	#gaph[4] = 0.2
	fig = FigArray(frameW, frameH, gapw, gaph)
	(W, H) = fig.dimensions()
	plt.figure(1, figsize=(W, H))
	
	estimlist = grab_files()

	ctr = 0

	plt.axis("off")
	
	
	for i in range(x):
		for j in range(y):
			
			#origin set in top-left corner
			a = plt.axes(fig.axes(i+1,j+1))
			
			dispim = estimlist[ctr]
				
			p = plt.imshow(dispim)
			
			a.xaxis.set_major_locator(plt.NullLocator())
			a.yaxis.set_major_locator(plt.NullLocator())
			plt.gray()  # overrides current and sets default
			
			
	
			ctr += 1
	
	
	
	plt.savefig(LOC+figure, dpi=150)
	plt.close()
	
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
	PlotOutput()
	
	
				
		
if __name__ == "__main__":
	
	main()