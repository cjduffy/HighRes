def darkflat(flat_field, dark_current, raw_style, style_type, exp_time, master_exp_time):
	
	##Function takes previously opened Flat, Dark, and Raw images, along with exposure time to perform the darkflat corrections. 
	
	import os
	from astropy.io import fits
	import numpy as np
	
	#Get Data
	flat_field_data = flat_field[0].data
	dark_current_data = dark_current[0].data
	
	##Open Raw Image
	if style_type == "single":
		raw_image = fits.open(raw_style)
		raw_image_data = raw_image[0].data
		
		#Scale Dark Current
		scaling_factor = np.divide(exp_time, master_exp_time)
		scaled_dark_current = np.multiply(scaling_factor, dark_current_data)
		
		#Perform Correction
		dark_sub = np.subtract(raw_image_data, scaled_dark_current)
		cor_image = np.divide(dark_sub, flat_field_data)
		
		#Write Corections
		hdu = fits.PrimaryHDU()
		hdu.data = cor_image
		hdu.writeto(raw_style+"_darkflat_corrected")
	
		return(0)
		
	elif style_type == "group":
		n = 1
		for file in raw_style:
			raw_image = fits.open(file)
			raw_image_data = raw_image[0].data
		
			#Scale Dark Current
			scaling_factor = np.divide(exp_time, master_exp_time)
			scaled_dark_current = np.multiply(scaling_factor, dark_current_data)
			
			#Perform Correction
			dark_sub = np.subtract(raw_image_data, scaled_dark_current)
			cor_image = np.divide(dark_sub, flat_field_data)
			
			#Write Corections
			hdu = fits.PrimaryHDU()
			hdu.data = cor_image
			filepath = (raw_style+"_darkflat_corrected_%d") %n
			hdu.writeto(filepath)
			
	return(0)
	
	
