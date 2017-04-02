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
	
def Auto_Hot_Pix_Correction(data_list, zero_number):
	import numpy as np
	from scipy.signal import convolve2d
	from astropy.io import fits
	import os
	
	if data_list[4].raw_data == 0:
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Raw Data")
		dialog.format_secondary_text("Please select raw data from the raw data input tab")
		response = dialog.run()
		dialog.destroy()
		return(1)
		
	for file in os.path.listdir(data_list[4].raw):
		histogram, bins = np.histogram(file, bins="auto")
		x = 0
		n = 0
		
		for x in range(0,len(histogram)):
			if histogram[x] != 0:
				highest_count = x
			else:
				pass
			x += 1
			
		for highest_count in range(0,highest_count):
			if histogram[highest_count] == 0:
				if n == zero_number:
					threshold = bins[highest_count]
				else:
					n += 1
			else:
				pass
			highest_count -= 1
			
		image = fits.open(file)
		array = image[0].data
		
		x = np.matrix('0 1 0; 1 0 1; 0 1 0')
		y = np.divide(x, 4)
		
		mean = convolve2d(arr, y, mode='same')
		
		array[array > threshold] = mean[array > threshold]
		
		hdu = fits.PrimaryHDU()
		hdu.data = array
		hdu.writeto(file, overwrite=True)
		
	return(0)
			
		
			
		
				
	
