; deconv_bench test batch 
loadct, 3
gamma_ct, 0.4

FLAT_FIELD_ERROR = ['0.00','0.03']
NPHOTONS = ['1E+07','1E+08']

foreach ff, FLAT_FIELD_ERROR do begin	
	foreach phot, NPHOTONS do begin
	
	tab_image = readfits('/Users/kstlaurent/NIRISS NRM/realer_images/MASK_NRM_OPD162_ff'+ff+'_F430M_realer_N'+phot+'_image.fits')
	TV, tab_image
	tab_psf = readfits('/Users/kstlaurent/NIRISS NRM/PSF/MASK_NRM.162.F430M.'+phot+'.0.0_bin_PSF.fits')

	NP = (size(tab_image))[1]
	Nbimages = 1;(size(tab_image))[3]

	; First deconvolution with a quadratic regularization 
	;tab_weights = dblarr(NP,NP,Nbimages) + 1D
	tab_weights = dblarr(NP,NP) + 1D
	un = dblarr(NP,NP) + 1D
	threshold = 1D-5
	nb_iter = 1000
	scale = 31.6
	delta = 1.00
	
	;size_i = (size(scales))[1]
	;size_j = (size(deltas))[1]
						
	; deconvolution with L1L2 regularization - with guess (real object)
	;table = dblarr(size_i,size_j)
							
	;window, 0, xs = NP*4, ys = NP*2, title= "Left: Current object estimation, Right: difference with the previous object estimation" 
	;L1-L2 regularization
	print, "FF: ",ff," Nphot: ",phot
			
	objet_estime = dblarr(NP,NP)
	objet_estime = deconv_bench(IMAGE = tab_image, PSF = tab_psf, WEIGHTS = tab_weights, /WHITE, SCALE = scale, DELTA = delta,/PROJECTION, /VMLM, /VISU, zoom = 2, /VERSION, THRESHOLD = threshold,  GUESS = objet_estime)
	writefits, '/Users/kstlaurent/NIRISS NRM/realer_estim/MASK_NRM_OPD162_ff'+ff+'_F430M_realer'+phot+'_estim.fits', objet_estime
			
	endforeach
endforeach

END
