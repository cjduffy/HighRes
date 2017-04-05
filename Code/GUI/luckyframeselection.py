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
		
	maximum = max(Fisher_Sum)
	
	if state == "retain":
		if not os.path.isdir(str(data_list_entry.data_filedata)+"/lucky_frames") == True:
			os.mkdir(str(data_list_entry.data_filedata)+"/lucky_frames")
	
	for file in os.listdir(data_list_entry.data_filedata):
		if file.endswith(".fits"): 
			percent = Fisher_Sum[p]/maximum * 100
			if percent < percentage:
				if state == "delete":
					source = data_list_entry.data_filedata+"/"+file
					os.remove(source)
			if percent > percentage:
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
			
	maximum = max(sobel_number)
	
	if state == "retain":
		if not os.path.isdir(str(data_list_entry.data_filedata)+"/lucky_frames") == True:
			os.mkdir(str(data_list_entry.data_filedata)+"/lucky_frames")
			
	for file in os.listdir(data_list_entry.data_filedata):
		if file.endswith(".fits"):
			entry = sobel_number[p]
			percent = entry/maximum * 100
			p += 1
			if percent < percentage:
				if state == "delete":
					source = data_list_entry.data_filedata+"/"+file
					os.remove(source)
			if percent > percentage:
				if state == "retain":
					source = data_list_entry.data_filedata+"/"+file
					destination = str(data_list_entry.data_filedata)+"/lucky_frames/"+file
					shutil.move(source, destination)
	
	return(0)
