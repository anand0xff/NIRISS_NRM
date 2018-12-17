; deconv_bench test batch 
loadct, 3
gamma_ct, 0.4

PUPILS = ['MASK_NRM','CLEARP']
FLAT_FIELD_ERROR = ['0.00','0.01']
NPHOTONS = ['1E+07','1E+08']
BAR = ['1.0','0.3','0.0']

foreach ff, FLAT_FIELD_ERROR do begin	
	foreach pup, PUPILS do begin 
		foreach phot, NPHOTONS do begin
			foreach bright, BAR do begin
	
				tab_image = readfits('/Users/kstlaurent/NIRISS NRM/N1068_Im/'+pup+'_OPD162_ff'+ff+'_F430M_N1068_N'+phot+'_noisy_bar'+bright+'_image.fits')
				TV, tab_image
				tab_psf = readfits('/Users/kstlaurent/NIRISS NRM/PSF/'+pup+'.162.F430M.'+phot+'.1.0_bin_PSF.fits')

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
				print, "FF: ",ff," Pupil: ",pup," Nphot: ",phot
			
				objet_estime = dblarr(NP,NP)
				objet_estime = deconv_bench(IMAGE = tab_image, PSF = tab_psf, WEIGHTS = tab_weights, /WHITE, SCALE = scale, DELTA = delta,/PROJECTION, /VMLM, /VISU, zoom = 2, /VERSION, THRESHOLD = threshold,  GUESS = objet_estime)
				writefits, '/Users/kstlaurent/NIRISS NRM/N1068_Estim/'+pup+'_OPD162_ff'+ff+'_F430M_N1068_N'+phot+'_noisy_bar'+bright+'.fits', objet_estime
			
			endforeach		
		endforeach
	endforeach
endforeach

END
