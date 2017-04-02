def master_creation(primary_data_entry, secondary_data_entry, master_entry):
	
	import numpy as np
	import os
	from astropy.io
	
	mean_prime = 0
	mean_secondary = 0
	mean_pair = [mean_prime, mean_secondary]
	data_entry = [primary_data_entry, secondary_data_entry]
	
	stage = 0
	
	for stage in range(0,1):
		counter = 0
		for file in dirs in data_entry[stage].data_filedata: 
			if file.startswith(str(data_entry[stage].data_type)):
				counter += 1
				im_fit = image.open(file)
				im_data = im_fit[0].data
				im_total = np.add(im_total, im_data)
				
		

	
