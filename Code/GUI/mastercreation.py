def master_creation(primary_data_entry, secondary_data_entry, master_entry):
	
	import numpy as np
	import os
	from astropy.io import fits
	
	mean_prime = 0
	mean_secondary = 0
	mean_pair = [mean_prime, mean_secondary]
	data_entry = [primary_data_entry, secondary_data_entry]
	
	stage = 0
	
	for stage in range(0,1):
		counter = 0
		for root, dirs, files in os.walk(data_entry[stage].data_filedata):
			for file in dirs:
				if file.endswith(".fits"):
					if file.startswith(str(data_entry[stage].data_type)):
						counter += 1
						im_fit = image.open(file)
						im_data = im_fit[0].data
						
						if counter == 1:
							im_total = np.zeros((im_data.shape)) 
						
						im_total = np.add(im_total, im_data)
		mean_pair[stage] = np.divide(im_total, counter)
		stage += 1
		
	master_im = np.subtract(mean_pair[0], mean_pair[1])
	hdu = fits.PrimaryHDU()
	hdu.data = master_im
	
	filename = "Master_"+str(primary_data_entry.data_type)+".fits"
	
	master_entry.set_master_filename = filename
	hdu.writeto(filename, overwrite=True)
	
	return(0)
		
				
				
				
		

	
