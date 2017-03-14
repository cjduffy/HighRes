import numpy as np
from scipy.fftpack import fft2, ifft2
from scipy.ndimage import rotate
import scipy.ndimage.interpolation as ndii 
import math
#Final version won't need PIL
from PIL import Image

def logpolar(image, i_0, j_0, p_n=None, t_n=None):
    (i_n, j_n) = image.shape[:2]
    
    i_c = max(i_0, i_n - i_0)
    j_c = max(j_0, j_n - j_0)
    d_c = (i_c ** 2 + j_c ** 2) ** 0.5

    if p_n == None:
        p_n = int(math.ceil(d_c))
    
    if t_n == None:
        t_n = j_n
    
    p_s = math.log(d_c) / p_n
    t_s = 2.0 * np.pi / t_n
    
    transformed = np.zeros((p_n, t_n) + image.shape[2:], dtype=image.dtype)

    for p in range(0, p_n):
        p_exp = math.exp(p * p_s)
        for t in range(0, t_n):
            t_rad = t * t_s

            i = int(i_0 + p_exp * math.sin(t_rad))
            j = int(j_0 + p_exp * math.cos(t_rad))

            if 0 <= i < i_n and 0 <= j < j_n:
                transformed[p, t] = image[i, j]

    return transformed
	

def FMI(data1, data2):
	try:
		max_x_1, max_y_1 = data1.shape
		max_x_2, max_y_2 = data2.shape
	except:
		max_x_1, max_y_1, colour = data1.shape
		max_x_2, max_y_2, colour = data2.shape
		
	##Calcylate the centres for both images
	centre_x_1 = max_x_1/2
	centre_y_1 = max_y_1/2
	
	centre_x_2 = max_x_2/2
	centre_y_2 = max_y_2/2
	
	LP1 = logpolar(data1, centre_x_1, centre_y_1)
	LP2 = logpolar(data2, centre_x_2, centre_y_2)
	
	##Fourier Time!
	
	transform_image_1 = fft2(LP1)
	transform_image_2 = fft2(LP2)
		
	phase_image_1 = np.imag(transform_image_1)
	phase_image_2 = np.imag(transform_image_2)
		
	if phase_image_1.shape != phase_image_2.shape:
		try:
			x1, y1 = phase_image_1.shape
			x2, y2 = phase_image_2.shape
			try:
				x = x2 - x1
				y = y2 - y1
				phase_image_1 = np.lib.pad(phase_image_1, ((x,0,), (y,0)), 'edge')
			except:
				x = x1 - x2
				y = y1 - y2
				phase_image_2 = np.lib.pad(phase_image_2, ((x,0,), (y,0)), 'edge')
			
		except:
			x1, y1, colour = phase_image_1.shape
			x2, y2, colour = phase_image_2.shape
			try:
				x = x2 - x1
				y = y2 - y1
				phase_image_1 = np.lib.pad(phase_image_1, ((x,0,), (y,0), (0,0) ), 'edge')
			except:
				x = x1 - x2
				y = y1 - y2
				phase_image_2 = np.lib.pad(phase_image_2, ((x,0,), (y,0), (0,0) ), 'edge')
	
	SPOMF = np.exp(np.subtract(phase_image_2, phase_image_1))
	iSPMF = ifft2(SPOMF)
	
	return iSPMF

##Image read in

##Currently Hard wired for something in my working directory as I have decided how best to loop this yet.
image1 = Image.open('scifestt.jpg')
image2 = Image.open('scifestt.jpg')

data1 = np.array((image1))
data2 = np.array((image2))

iSPMF1 = FMI(data1, data2)

try:
	rotation, scale = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
except:
	rotation, scale, colour = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
scaling_factor = np.exp(scale)
print(rotation)
print(scaling_factor)

try:
	n, m = (data2.shape/scaling_factor)
	n = int(n)
	m = int(m)
	scaled_image = data2.resize((n,m))
	
except:
	n, m, colour = (data2.shape/scaling_factor)
	n = int(n)
	m = int(m)
	colour = int(colour)
	scaled_image = np.resize(data2, (n,m,colour))
	

scaled_image_2 = scaled_image
rot1 = rotate(scaled_image, rotation, axes=(0,1), reshape = False)
rot2 = rotate(scaled_image_2, rotation+180, reshape = False)

iSPMF2 = FMI(data1, rot1)
iSPMF3 = FMI(data1, rot2)

A = np.amax(iSPMF2)
B = np.amax(iSPMF3)
