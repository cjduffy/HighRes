def filtering(fits_image, a, b):
	import numpy as np
	from astropy.io import fits
	from scipy.fftpack import fft2, ifft2
	from scipy import ndimage
	import math
	
	open_image = fits.open(fits_image)
	image = open_image[0].data
	if image.ndim == 3:
		image = image[:,:,0] 
	image = np.nan_to_num(image)
	
	x, y = image.shape
	high_pass = Filter(image, x, y, a, b)
	image = image.astype('float32')
	FT_image = fft2(image)
	real = FT_image.real
	imaginary = FT_image.imag
	filtered_real = np.multiply(real, high_pass)
	filtered_imag = np.multiply(imaginary, high_pass)
	filtered_complex = np.zeros_like(image, dtype=complex)
	for n in range(0,y-1):
		for m in range(0,x-1):
			filtered_complex[m,n] = complex(filtered_real[m,n], filtered_imag[m,n])
			
	output = ifft2(filtered_complex)
	output = output.astype('float32')
	
	new_file = fits_image.replace(".fits", "_filtered.fits")
	
	hdu = fits.PrimaryHDU
	hdu.data = output
	hdu.writeto(new_file, overwrite=True)
	return(0)

def Filter(image, x, y, a, b):
	high_pass = np.zeros_like(image)
	for m in range(1, y):
		for n in range(1, x):
			high_pass[n,m] = 1/(1+(a/math.sqrt((n**2 + m**2)))**(2*b))
	return high_pass


