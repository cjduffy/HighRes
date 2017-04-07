def Man_Hot_Pix_Correction(image_file, thresholds):
	import numpy as np
	from scipy.signal import convolve2d
	from astropy.io import fits
	
	x = 0
	threshold_total = 0
	for x in range(0, len(thresholds)-1):
		threshold_total += int(thresholds[x])
		x += 1
	
	threshold = threshold_total/len(thresholds)
	image = fits.open(image_file)
	array = image[0].data
	
	x = np.matrix('0 1 0; 1 0 1; 0 1 0')
	y = np.divide(x, 4)
	
	mean = convolve2d(array,y, mode='same')

	array[array > threshold] = mean[array > threshold]
	
	hdu = fits.PrimaryHDU()
	hdu.data = array
	hdu.writeto(image_file, overwrite = True)
	
	return(0)
	
def Auto_Hot_Pix_Correction(image_file, zero_number):
	import numpy as np
	from scipy.signal import convolve2d
	from astropy.io import fits
	import os
	
	image = fits.open(image_file)
	array = image[0].data
	
	histogram, bins = np.histogram(array, bins="auto")
	x = 0
	n = 0
	
	for x in range(0, len(histogram)):
		if histogram[x] != 0:
			highest_count = x
		x += 1
	
	for highest_count in range(0, highest_count):
		if histogram[highest_count] == 0:
			if n == zero_number:
				threshold = bins[highest_count]
			else:
				n += 1
		highest_count -= 1
	
	x = np.matrix('0 1 0; 1 0 1; 0 1 0')
	y = np.divide(x, 4)
	
	mean = convolve2d(array, y, mode='same')
	
	array[array > threshold] = mean[array > threshold]
	
	hdu = fits.PrimaryHDU()
	hdu.data = array
	hdu.writeto(image_file, overwrite=True)
	
	return(0)
			
		
			
		
				
	
