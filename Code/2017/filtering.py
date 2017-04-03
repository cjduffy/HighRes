import numpy as np
from astropy.io import fits
from scipy.fftpack import fft2, ifft2
from scipy import ndimage
from scipy.signal import butter
import math

def filtering(image):
	x, y = image.shape
	high_pass = Filter(image, x, y)
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
	return output

def Filter(image, x, y):
	high_pass = np.zeros_like(image)
	for m in range(1, y):
		for n in range(1, x):
			high_pass[n,m] = 1/(1+(25/math.sqrt((n**2 + m**2)))**(2*5))
	return high_pass

def imshow(im1, im2, cmap=None, **kwargs):
	"""Plot images using matplotlib."""
	from matplotlib import pyplot
	#if cmap is None:
		#cmap = 'rainbow'
	pyplot.subplot(121)
	pyplot.title("Oringial")
	pyplot.imshow(im1, cmap, **kwargs)
	pyplot.subplot(122)
	pyplot.title("Filtered")
	pyplot.imshow(im2, cmap, **kwargs)
	pyplot.show()

image = 'frame_1_43.fits'
image = fits.open(image)
image = image[0].data
image_decoloured = image[:,:,0]
image_filtered = filtering(image_decoloured)
imshow(image_decoloured, image_filtered)


