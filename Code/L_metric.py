import numpy as np
from astropy.io import fits

LOC = '/Users/kstlaurent/Box Sync/NIRISS NRM/'
ESTIM_FILE = 'L1L2space/estim/%s_OPD%d_ff%.2f_L%.2f_C%.2f_s%02dd%02d.fits'#(pup,OPD,ff,NL,C,i,j)
OBJECT_FILE = 'Objects/L%.1f_C%.1f_object.fits'#(NL,C)
SUPPORT_FILE = 'Supports/L%.1f_support.fits'#(NL)
METRIC_FILE = 'L1L2space/metric/%s_OPD%d_ff%.2f_L%.2f_C%.2f_s%.2fd%.2f.fits'#(pup,OPD,ff,NL,C,i,j)

fov = 81
ov = 11

PUPILS = ['MASK_NRM','CLEARP']
OP_PATH_DIFF = [162,810]
FLAT_FIELD_ERROR = [0.00,0.01,0.03]
LENGTH = [1.0,1.5,2.0,2.5,3.0,4.0]
CONTRAST = [2.0,3.0,4.0,5.0]

scales = [3.16,10,31.6,100,316]
deltas = [0.30,0.60,1.00,1.50,2.00]
N = len(scales)
M = len(deltas)
i = 2
j = 2

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

def make_support(r):
	sup = r+1
	ctr = (fov/2,fov/2)
	pupil = makedisk(fov,ctr=ctr,radius=sup)	
	fits.PrimaryHDU(data=pupil).writeto(LOC+SUPPORT_FILE%(r), clobber=True)		
	return pupil

def rebin(a, bin_factor): 
	shape = a.shape[0]//bin_factor
	sh = shape,a.shape[0]//shape,shape,a.shape[1]//shape
	return a.reshape(sh).sum(-1).sum(1)

def calc_real(NL,C):
	object = fits.getdata(LOC+OBJECT_FILE%(NL,C))
	return rebin(object,ov)
	
def calc_metric(a,b,k,support=None):
	if support is None:
		support = np.ones(a.shape)
	
	supportidx = np.where(support==1)		
	metric = np.power(abs(a-b),k)
	return metric.sum()/len(supportidx[0])
	
def main():
	
	for pup in PUPILS:
		for OPD in OP_PATH_DIFF:
			for ff in FLAT_FIELD_ERROR:
				print pup,',', OPD,',',ff
				metric_list = []
				for NL in LENGTH:
					support = make_support(NL)
					for C in CONTRAST:
						
						estim = fits.getdata(LOC+ESTIM_FILE%(pup,OPD,ff,NL,C,i,j))
						real_obj = calc_real(NL,C)
						metric_num = calc_metric(estim,real_obj,2,support)
						metric_list.append(metric_num)		
						print NL,C, '%.3f'%metric_num
						
						fits.PrimaryHDU(data=metric_array).writeto(LOC+METRIC_FILE%(pup,OPD,ff,NL,C,scales[i],deltas[j]), clobber=True)

if __name__ == "__main__":
	main()
				
				
				