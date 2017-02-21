def Sobel(Image): 
	
	import numpy as np
	import scipy import ndimage
	from astropy.io import FITS 
	
	#image = im.astype('int32') if we ever have/need higher precision
	
	dx = ndimage.sobel(Image, 0, mode="constant") 
	dy = ndimage.sobel(Image, 1, mode="constant") 
	mag = np.hypot(dx,dy)
