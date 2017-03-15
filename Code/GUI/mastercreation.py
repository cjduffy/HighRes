def master_creation(data_list, master_structure, mode):
	
	import numpy as np
	import os
	from astropy.io import fits
	
	if mode == "dark":
		beginning_stage = 0
		end_stage = 1
	elif mode == "flat":
		beginning_stage = 2
		end_stage = 3
	else:
		return("Mode Error")
		
	stage = beginning_stage
	
	if mode == "flat":
		target = stage - beginning_stage 
	
	mean_prime = 0
	mean_second = 0
	
	mean_pair = [mean_prime, mean_second]
	
	for stage in range(beginning_stage,end_stage):
		counter = 0
		for file in dirs in data_list[stage].data:
			if file.startswith(str(data_list[stage].data_type)):
				counter += 1
				im_fit = fits.open(file)
				im_data = im_fit[0].data
				im_total = np.add(im_total, im_data)
				
		if mode == "dark":
			mean_pair[stage] = np.divide(im_total, counter)
			
		elif mode == "flat":
			mean_pair[target] = np.divide(im_total, counter)
			target += 1
		
		stage += 1	
			
	master_im = np.subtract(mean_pair[0], mean_pair[1])
		
	hdu = fits.PrimaryHDU()
	hdu.data = master_im

	if mode = "dark":
		filename = "Master"+str(data_list[0].data_type)+".fits"
	elif mode = "flat":
		filename = "Master"+str(data_list[1].data_type)+".fits"	
	
	master_structure.set_master_filename(mode, filename)
	hdu.writeto(filename, overwrite = True)
	
	return(master_structure)
		

	
