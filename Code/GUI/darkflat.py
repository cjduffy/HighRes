def darkflat(flat_field, dark_current, raw_image, exp_time, master_exp_time):
	
	##Function takes previously opened Flat, Dark, and Raw images, along with exposure time to perform the darkflat corrections. 
	
	import os
	from astropy.io import fits
	import numpy as np
	
	#Scale Dark Current
	scaling_factor = np.divide(exp_time, master_exp_time)
	scaled_dark_current = np.multiply(scaling_factor, dark_current)
	
	#Perform Correction
	dark_sub = np.subtract(raw_image, scaled_dark_current)
	cor_image = np.divide(dark_sub, flat_field)
	
	#Write Corections
	hdu = fits.PrimaryHDU()
	hdu.data = cor_image
	hdu.writeto("darkflat_corrected_"+Raw)
	
	return(0)
