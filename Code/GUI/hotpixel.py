def Man_Hot_Pix_Correction(image_file, thresholds):
	import numpy as np
	from scipy.signal import convolve2d
	from astropy.io import fits
	
	threshold = np.average(thresholds)
	
	image = fits.open(image_file)
	array = image[0].data
	
	x = np.matrix('0 1 0; 1 0 1; 0 1 0')
	y = np.divide(x, 4)
	
	mean = convolve2d(arr,y, mode='same')

	array[array > threshold] = mean[array > treshold]
	
	hdu = fits.PrimaryHDU()
	hdu.data = array
	hdu.writeto(file, overwrite = True)
	
	return(0)
	
def Auto_Hot_Pix_Correction():
	print("things to happen")
