def fisher_selection(data_list_entry, percentage, state):
	
	import numpy as np
	import os
	from astropy.io import fits
	import shutil
	from PIL import Image
	
	n = 1
	m = 1
	l = 1
	p = 1
	
	fisher_sum = 0
	Fisher_Sum = dict()
	
	for file in os.listdir(data_list_entry):
		if file.endswith(".png"):
			filepath = data_list_entry+"/"+file
			image = Image.open(filepath)
			image_data = np.array(image)
			
			if image_data.ndim == 3:
				image_data = image_data[:,:,0]
			
			x,y = image_data.shape
			normalised_image = np.zeros((x,y))
			sum_pixels = np.sum(image_data)
			
			for n in range(0,x):
				for m in range(0,y):
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
		if not os.path.isdir(str(data_list_entry)+"/lucky_frames_fisher") == True:
			os.mkdir(str(data_list_entry)+"/lucky_frames_fisher")
	
	for file in os.listdir(data_list_entry):
		if file.endswith(".png"): 
			if Fisher_Sum[p] < threshold:
				if state == "delete":
					source = data_list_entry+"/"+file
					os.remove(source)
			if Fisher_Sum[p] > threshold:
				if state == "retain":
					source = data_list_entry+"/"+file
					destination = str(data_list_entry)+"/lucky_frames_fisher/"+file
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
	from PIL import Image
	
	l = 1
	p = 1
	sobel_number = dict()
	
	for file in os.listdir(data_list_entry):
		if file.endswith(".png"):
			filepath = data_list_entry+"/"+file
			image_data = Image.open(filepath)
			#image_data = image[0].data
			
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
		if not os.path.isdir(str(data_list_entry)+"/lucky_frames_sobel") == True:
			os.mkdir(str(data_list_entry)+"/lucky_frames_sobel")
			
	for file in os.listdir(data_list_entry):
		if file.endswith(".png"):
			if sobel_number[p] < threshold:
				if state == "delete":
					source = data_list_entry+"/"+file
					os.remove(source)
			if sobel_number[p] > threshold:
				if state == "retain":
					source = data_list_entry+"/"+file
					destination = str(data_list_entry)+"/lucky_frames_sobel/"+file
					shutil.move(source, destination)
			p += 1
	return(0)

import timeit

print(timeit.timeit("sobel_selection('Images', 50, 'retain')", setup = "from __main__ import sobel_selection", number = 1))
#print(timeit.timeit("fisher_selection('Images', 50, 'retain')", setup = "from __main__ import fisher_selection", number = 1))
