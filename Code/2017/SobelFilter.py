import numpy as np

Image = np.array([[1,2],[1,2]])

def Sobel(Image): 
	
	import numpy as np
	from scipy import ndimage
	from astropy.io import fits 
	
	#image = im.astype('int32') if we ever have/need higher precision
	
	dx = ndimage.sobel(Image, 0, mode="constant") 
	dy = ndimage.sobel(Image, 1, mode="constant") 
	mag = np.hypot(dx,dy)
	
	return(mag)

n = Sobel(Image)
print(n)
