def master_creation(primary_data_entry, secondary_data_entry, master_entry):
	
	import numpy as np
	import os
	from astropy.io import fits
	
	im_total = np.zeros((1,1))
	mean_prime = 0
	mean_secondary = 0
	mean_pair = [mean_prime, mean_secondary]
	data_entry = [primary_data_entry, secondary_data_entry]
	
	stage = 0
	
	for stage in range(0,2):
		if os.path.isfile(data_entry[stage].data_filedata):
			im_fit = fits.open(data_entry[stage].data_filedata)
			im_data = im_fit[0].data
			mean_pair[stage] = im_data
		else:	
			counter = 0
			for root, dirs, files in os.walk(data_entry[stage].data_filedata):
				for filename in files:
					if filename.endswith(".fits"):
						if filename.startswith(str(data_entry[stage].data_type)):
							full_filename = os.path.join(root, filename)
							counter += 1
							im_fit = fits.open(full_filename)
							im_data = im_fit[0].data
							im_total = np.add(im_total, im_data)
			if counter == 0:
				print("Counter zero!")
				return(1)
			else:
				mean_pair[stage] = np.divide(im_total, counter)
		stage += 1
		
	master_im = np.subtract(mean_pair[0], mean_pair[1])
	hdu = fits.PrimaryHDU()
	hdu.data = master_im
	
	file_name = "Master_"+str(primary_data_entry.data_type)+".fits"
	
	master_entry.set_master_filename(file_name)
	hdu.writeto(file_name, overwrite=True)
	
	return(0)
