def darkflat_correction(masters, data_list_entry):
	
	import os
	from astropy.io import fits
	import numpy as np
	
	if masters[0].master_data.shape == 0:
		master_image = fits.open(masters[0].master_filename)
		masters[0].set_master_data(master_image)
		
	if masters[1].master_data.shape == 0:
		master_image_2 = fits.open(masters[1].master_filename)
		masters[1].set_master_data(master_image_2)
	
	if data_list_entry.data_mode == "single":
		raw_image = fits.open(data_list_entry.data_filedata)
		raw_image_data = raw_image[0].data
		
		scaling_factor = np.divide(exp_time, master_exp_time)
		scaled_dark_current = np.multiply(scaling_factor, masters[0].data)
		
		dark_sub = np.subtract(raw_image_data, scaled_dark_current)
		cor_image = np.divide(dark_sub, masters[1].data)
		
		new_filename = file.replace(".fits", "_darkflat_corrected.fits")
		
		hdu = fits.PrimaryHDU()
		hdu.data = cor_image
		hdu.writeto(new_filename, overwrite = True)
		
		data_list_entry.set_data_filedata(new_filename)
		
	elif data_list_entry.data_mode == "group":
		if os.path.isdir(data_list_entry.data_filedata+"/lucky_frames") == True:
			folder = data_list_entry.data_filedata+"/lucky_frames"
		else:
			folder = data_list_entry.data_filedata
			
		for file in os.listdir(folder):
			filepath = folder+"/"+file
			
			raw_image = fits.open(filepath)
			raw_image_data = raw_image[0].data
			
			scaling_factor = np.divide(exp_time, master_exp_time)
			scaled_dark_current = np.multiply(scaling_fator, masters[0].data)
			
			dark_sub = np.subtract(raw_image_data, scaled_dark_current)
			cor_image = np.divide(dark_sub, masters[1].data)
			
			if not os.path.isdir(folder+"/darkflat_corrected") == True:
				os.mkdir(folder+"/darkflat_corrected")
			
			new_filepath = folder+"/darkflat_corrected/"+file
			
			hdu = fits.PrimaryHDU()
			hdu.data = cor_image
			hdu.writeto(new_filepath, overwrite = True)
			
			data_list_entry.set_data_filedata(folder+"/dark_flatcorrected")
	
	return(0)
	
