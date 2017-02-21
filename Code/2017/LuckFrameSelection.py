import numpy as np

n=1
m=1
fisher_sum = 0

image = np.array([[1,2],[1,2]])
sum_pixels = np.sum(image)

x,y = image.shape
normalised_image = np.zeros((x, y))


for n in range (1, x):
	for m in range (1, y):
		pixel = image[n,m]
		normalised_image[n,m] = np.divide(pixel, sum_pixels)
			
sqrt_img = np.sqrt(normalised_image)
grad_img = np.gradient(sqrt_img)
mag_img = np.abs(grad_img)
square_img = mag_img**2
fisher_sum += np.sum(square_img)
Fisher_Sum = 4*fisher_sum
print(Fisher_Sum)
	
		
