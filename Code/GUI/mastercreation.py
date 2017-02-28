def master_creation(folder, folder_2, Imtype, Imtype_2):
	
	import numpy as np
	import os 
	from astropy.io import fits
	
	n = 0
	m = 0
	
	condition = True
	condition_2 = True
	
	while condition = True: 
		for file in dirs in folder:
			filename = str(Imtype)+"1_1.fits"
			if os.path_isfile(filename):
				test = fits.open(filename)
				testdata = test[0].data
				size = testdata.shape 
				image = np.zeros(size)
				condition = False

	while condition_2 = True:
		for file in dirs in folder:
			filename_2 = str(Imtype_2)+"1_1.fits"
			if os.path_isfile(filename_2):
				test_2 = fits.open(filename_2)
				testdata_2 = test[0].data
				size_2 = testdata_2.shape
				image_2 = np.zeros(size_2)
				condition = False
	
	for file in dirs in folder:
		if file.startswith(Imtype):
			n += 1
			im_fit = fits.open(file)
			im_data = im_fit[0].data
			im_total = np.add(im_total, im_data)
			
	for file in dirs in folder_2: 		
		if file.startswith(Imtype_2):
			m += 1
			im_fit_2 = fits.open(file)
			im_data_2 = im_fit_2[0].data
			im_total_2 = np.add(im_total_2, im_data_2)
			
	mean_im = np.divide(im_total, n) 
	mean_im_2 = np.divide(im_total_2, m) 
	
	master_im = np.subtract(mean.im, mean_im_2)
	
	hdu = fits.PrimaryHDU()
	hdu.data = master_im
	hdu.writeto("Master_"+str(Imtype)+".fits", overwrite = True)
			
			
		
	
	
