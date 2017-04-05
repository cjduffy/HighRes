def fisher_selection(data_list_entry, percentage, state):
	
	import numpy as np
	import os
	from astropy.io import fits
	import shutil 
	
	n = 1
	m = 1
	l = 1
	p = 1
	
	fisher_sum = 0
	Fisher_Sum = dict()
	
	for file in os.listdir(data_list_entry.data_filedata):
		if file.endswith(".fits"):
			filepath = data_list_entry.data_filedata+"/"+file
			image = fits.open(filepath)
			image_data = image[0].data
			
			if image_data.ndim == 3:
				image_data = image_data[:,:,0]
			
			x,y = image_data.shape
			normalised_image = np.zeros((x,y))
			
			sum_pixels = np.sum(image_data)
			
			for n in range(1,x):
				for m in range(1,y):
					pixel = image_data[n,m]
					normalised_image[n,m] = np.divide(pixel,sum_pixels)
					
			sqrt_img = np.sqrt(normalised_image)
			grad_img = np.gradient(sqrt_img)
			mag_img = np.abs(grad_img)
			square_img = mag_img**2
			fisher_sum = np.sum(square_img) 
			Fisher_Sum[l] = 4*fisher_sum
			l += 1
		
	maximum = max(Fisher_Sum.values())
	minimum = min(Fisher_Sum.values())
	percentage_step = (maximum - minimum)/100
	steps_to_take = percentage*percentage_step
	threshold = minimum+steps_to_take
	
	if state == "retain":
		if not os.path.isdir(str(data_list_entry.data_filedata)+"/lucky_frames") == True:
			os.mkdir(str(data_list_entry.data_filedata)+"/lucky_frames")
	
	for file in os.listdir(data_list_entry.data_filedata):
		if file.endswith(".fits"): 
			if Fisher_sum[p] < threshold:
				if state == "delete":
					source = data_list_entry.data_filedata+"/"+file
					os.remove(source)
			if Fisher_sum[p] > threshold:
				if state == "retain":
					source = data_list_entry.data_filedata+"/"+file
					destination = str(data_list_entry.data_filedata)+"/lucky_frames/"+file
					shutil.move(source, destination)
			p += 1
			
	return(0)
	
def sobel_selection(data_list_entry, percentage, state):
	
	import numpy as np
	import os
	from astropy.io import fits
	from scipy import ndimage
	import math
	import shutil
	
	l = 1
	p = 1
	sobel_number = dict()
	
	for file in os.listdir(data_list_entry.data_filedata):
		if file.endswith(".fits"):
			filepath = data_list_entry.data_filedata+"/"+file
			image = fits.open(filepath)
			image_data = image[0].data
			
			m = 1
			dx = ndimage.sobel(image_data, 0, mode="constant")
			dy = ndimage.sobel(image_data, 1, mode="constant")
			mag = np.hypot(dx,dy)
			
			average_pixel_value = np.mean(mag)
			sobel_number[l] = average_pixel_value
			
			l += 1
			
	maximum = max(sobel_number.values())
	minimum = min(sobel_number.values())
	percentage_step = (maximum - minimum)/100
	steps_to_take = percentage*percentage_step
	threshold = minimum+steps_to_take

	
	if state == "retain":
		if not os.path.isdir(str(data_list_entry.data_filedata)+"/lucky_frames") == True:
			os.mkdir(str(data_list_entry.data_filedata)+"/lucky_frames")
			
	for file in os.listdir(data_list_entry.data_filedata):
		if file.endswith(".fits"):
			if sobel_number[p] < threshold:
				if state == "delete":
					source = data_list_entry.data_filedata+"/"+file
					os.remove(source)
			if sobel_number[p] > threshold:
				if state == "retain":
					source = data_list_entry.data_filedata+"/"+file
					destination = str(data_list_entry.data_filedata)+"/lucky_frames/"+file
					shutil.move(source, destination)
			p += 1
	return(0)
