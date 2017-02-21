def darkflat(Flat, Dark, Raw, Exp_Time, Master_Exp_Time): 
	
	import os
	from astropy.io import fits
	import numpy as np
	
	#Image Read ins
	flat_field = fits.open(Flat)
	dark_current = fits.open(Dark)
	raw_image = fits.open(Raw)
	
	#Perform Correction
	dark_sub = np.subtract(raw_image, dark_current)
	cor_image = np.divide(dark_sub, flat_field)
	
	#Write Corections
	hdu = fits.PrimaryHDU()
	hdu.data = cor_image
	hdu.writeto("darkflat_corrected_"+Raw)
	
	return(0)
