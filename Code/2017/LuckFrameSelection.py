import numpy as np
import numdifftools as nd

n=1
m=1

image = np.array([[1,2],[1,2]])
sum_pixels = np.sum(image)

x,y = image.shape
normalised_image = zeros(x,y)

for n in range (1,x):
	for m in range (1, y):
		for n in range (1, x):
			for m in range (1, y):
				pixel = image[n,m]
				normalised_image = np.divide(pixel, sum_pixels)
			
		sqrt_img = np.sqrt(normalised_image)
		print(sqrt_img)
		grad_img = np.Gradient(sqrt_img)
		print(grad_img)
		mag_img = abs(grad_img)
		square_img = mag_img**2
		fisher_sum += square_img
		Fisher_Sum = 4*fisher_sum
	
		
