; deconv_bench test batch 
loadct, 3
gamma_ct, 0.4

LENGTH = ['1.00','1.50','2.00','2.50','3.00','4.00']
CONTRAST = ['2.0','3.0','4.0','5.0']
PUPILS = ['MASK_NRM','CLEARP']
OP_PATH_DIFF = ['162','810']
FLAT_FIELD_ERROR = ['0.00','0.01','0.03']
Nphotons = ['1E+04','1E+05','1E+06','1E+07']

foreach pup, PUPILS do begin
	foreach opd, OP_PATH_DIFF do begin
		foreach ffe, FLAT_FIELD_ERROR do begin
			foreach phot, NPHOTONS do begin
				foreach len, LENGTH do begin
					foreach con, CONTRAST do begin
								
						tab_image = readfits('/Users/kstlaurent/NIRISS NRM/Images/'+pup+'_OPD'+opd+'_ff'+ffe+'_L'+len+'_C'+con+'_N'+phot+'_noisy_image.fits')
						TV, tab_image
						tab_psf = readfits('/Users/kstlaurent/NIRISS NRM/PSF/'+pup+'.'+opd+'.F430M.'+phot+'.'+con+'_bin_PSF.fits')

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
						
						print, pup, " OPD: ",opd, "FF: ",ffe, " Nphot: ",phot, " L: ", len, " C: "
			
						objet_estime = dblarr(NP,NP)
						objet_estime = deconv_bench(IMAGE = tab_image, PSF = tab_psf, WEIGHTS = tab_weights, /WHITE, SCALE = scale, DELTA = delta,/PROJECTION, /VMLM, /VISU, zoom = 2, /VERSION, THRESHOLD = threshold,  GUESS = objet_estime)
						writefits, '/Users/kstlaurent/NIRISS NRM/Estim/'+pup+'_OPD'+opd+'_ff'+ffe+'_L'+len+'_C'+con+'_N'+phot+'_noisy_estim.fits', objet_estime
					
					endforeach
				endforeach
			endforeach		
		endforeach
	endforeach
endforeach

END
