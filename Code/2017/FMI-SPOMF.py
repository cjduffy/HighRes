import numpy as np
from scipy.fftpack import fft2, ifft2
from scipy.ndimage import rotate
import scipy.ndimage.interpolation as ndii 
import math
#Final version won't need PIL
from PIL import Image

def logpolar(image):

	
	##Initialise X Counter
	x = 1
	
	##Get Shape of Image
	max_x, max_y = image.shape
	Log_Polar_Image = np.zeros((max_x, max_y))
	
	##Calculate the centre position
	center_x = max_x/2
	center_y = max_y/2
	
	##Loop Through x and y:
	for x in range(1,max_x):
		y = 1
		for y in range(1,max_y):
			x_pos = x - center_x
			y_pos = y - center_y
			
			r = math.sqrt(x_pos**2 + y_pos**2)
			if x_pos != 0:
				a_in = math.fabs(y_pos/x_pos)
				a = np.arctan(a_in)
			else:
				a = 1
			#ep = math.log10(r)
			
			new_x = [r*np.cos(a)]
			new_y = [r*np.sin(a)]
	ndii.map_coordinates(image, [new_x, new_y], output=Log_Polar_Image)		
			
	return(Log_Polar_Image)
	

def FMI(data1, data2):
	
	LP1 = logpolar(data1)
	LP2 = logpolar(data2)
	
	##Fourier Time!
	
	transform_image_1 = fft2(LP1)
	transform_image_2 = fft2(LP2)
		
	phase_image_1 = np.imag(transform_image_1)
	phase_image_2 = np.imag(transform_image_2)
		
	if phase_image_1.shape != phase_image_2.shape:
		x1, y1 = phase_image_1.shape
		x2, y2 = phase_image_2.shape
		try:
			x = x2 - x1
			y = y2 - y1
			phase_image_1 = np.lib.pad(phase_image_1, ((x,0), (y,0)), 'edge')
		except:
			x = x1 - x2
			y = y1 - y2
			phase_image_2 = np.lib.pad(phase_image_2, ((x,0), (y,0)), 'edge')
		
	
	SPOMF = np.exp(np.array(np.subtract(phase_image_2, phase_image_1), dtype=np.float128))
	iSPMF = ifft2(np.array((SPOMF), dtype=np.float64))
	
	return iSPMF, #log_base

##Image read in

##Currently Hard wired for something in my working directory as I have decided how best to loop this yet.
image1 = Image.open('outfile.jpg')
image2 = Image.open('outfile2.jpg')

data1 = np.array((image1), dtype=np.float64)
data2 = np.array((image2), dtype=np.float64)

iSPMF1 = FMI(data1, data2)


rotation, scale = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
scaling_factor = np.exp(scale)


n, m = (data2.shape/scaling_factor)
n = int(n)
m = int(m)


scaled_image = np.resize(data2, (m,n))
scaled_image_2 = scaled_image

rot1 = rotate(scaled_image, rotation)
rot2 = rotate(scaled_image_2, rotation+180)

iSPMF2 = FMI(data1, rot1)
iSPMF3 = FMI(data1, rot2)

rotation1, scale1 = np.unravel_index(np.argmax(iSPMF2), iSPMF2.shape)
rotation2, scale2 = np.unravel_index(np.argmax(iSPMF3), iSPMF3.shape)

A = np.amax(iSPMF2)
B = np.amax(iSPMF3)
