def fisher_selection(data_list, percentage, state="Delete"):
	import numpy as np
	import os
	from astropy.io import FITS
	
	n = 1
	m = 1
	l = 1
	x = 1
	fisher_sum = 0
	Fisher_Sum = dict()
	
	folder = data_list[4].raw_data
	
	for file in folder:
		image = fits.open(file)
		image_data = image[0].data
		
		x,y = image.shape
		normalised_image = np.zeros((x,y))
		
		sum_pixels = np.sum(image)
		
		for n in range (1, x):
			for m in range (1, y):
				pixel = image[n,m]
				normalised_image[n,m] = np.divide(pixel,sum_pixels)
				
		sqrt_img = np.sqrt(normalised_image)
		grad_img = np.grad(sqrt_img)
		mag_img = np.mag(grad_img)
		square_img = mag_img**2
		fisher_sum = np.sum(square_img) 
		Fisher_Sum[l] = 4*fisher_sum
		l += 1
		
	maximum = max(Fisher_Sum)
	
	if state == "Retain":
		if not os.path.exists(folder/lucky_frames):
			os.mkdir(folder/lucky_frames)

	for file in folder:
		if file.endswith(".fits"):
			percent = Fisher_Sum[x] / maximum
			if percent < percentage:
				if state == "Delete":
					os.remove(file)
				elif state == "Retain":
					destination = folder+"/"+"lucky_frames/"+file
					os.rename(file, destination)
			x += 1
			
def sobel_selection(folder, percentage, state="Delete"):
	import numpy as np 
	import os
	from astropy.io import FITS
	from scipy import ndimage
	
	l = 1
	x = 1
	sobel_number = dict()
	
	folder = data_list[4].raw_data
	
	for file in folder:
		m = 1
		dx = ndimage.sobel(file, 0, mode="constant")
		dy = ndimage.sobel(file, 1, mode="constant")
		mag = hypot(dx,dy)
		value, edge = np.histogram(mag, bins=auto)
		bin_number = len(value)
		number_relevent_bins = np.floor(np.multiply(bin_number, percentage))
		for m in range(1,number_relevent_bins):
			new_value[m] = value[len(value) - m]
		sobel_number[l] = np.mean(new_value)
		l += 1 
		
	maximum = max(sobel_number)
	
	if state == "Retain":
		if not os.path.exists(folder/lucky_frames):
			os.mkdir(folder/lucky_frames)

	for file in folder:
		if file.endswith(".fits"):
			percent = Fisher_Sum[x] / maximum
			if percent < percentage:
				if state == "Delete":
					os.remove(file)
				elif state == "Retain":
					destination = folder+"/"+"lucky_frames/"+file
					os.rename(file, destination)
			x += 1
			
			
		
 
	
