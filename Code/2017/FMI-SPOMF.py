import numpy as np
from scipy.fftpack import fft2, ifft2
from scipy.ndimage import rotate
import scipy.ndimage.interpolation as ndii 
import math
from scipy.signal import convolve2d
#Final version won't need PIL
from PIL import Image

def _nd_window(data, filter_function):
    """
    Performs an in-place windowing on N-dimensional spatial-domain data.
    This is done to mitigate boundary effects in the FFT.

    Parameters
    ----------
    data : ndarray
           Input data to be windowed, modified in place.
    filter_function : 1D window generation function
           Function should accept one argument: the window length.
           Example: scipy.signal.hamming
    """
    for axis, axis_size in enumerate(data.shape):
        # set up shape for numpy broadcasting
        filter_shape = [1, ] * data.ndim
        filter_shape[axis] = axis_size
        window = filter_function(axis_size).reshape(filter_shape)
        # scale the window intensities to maintain image intensity
        window = np.power(window, (1.0/data.ndim))
        data = data * np.float64(window)
        
    return data

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
	
	try:
		data1_W = _nd_window(data1, np.hanning)
		data2_W = _nd_window(data2, np.hanning)
	except:
		data1_W = _nd_window(data1[:,:,0], np.hanning)
		data2_W = _nd_window(data2[:,:,0], np.hanning)
	
	LP1 = logpolar(data1_W, centre_x_1, centre_y_1)
	LP2 = logpolar(data2_W, centre_x_2, centre_y_2)
	
	##Fourier Time!
	
	transform_image_1 = fft2(LP1)
	transform_image_2 = fft2(LP2)
		
	phase_image_1 = transform_image_1
	phase_image_2 = transform_image_2
		
	if phase_image_1.shape != phase_image_2.shape:
		try:
			x1, y1 = phase_image_1.shape
			x2, y2 = phase_image_2.shape
			try:
				x = x2 - x1
				y = y2 - y1
				phase_image_1 = np.lib.pad(phase_image_1, ((x,0,), (y,0) ), 'edge')
			except:
				x = x1 - x2
				y = y1 - y2
				phase_image_2 = np.lib.pad(phase_image_2, ((x,0,), (y,0) ), 'edge')
			
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
	#SPOMF = np.multiply(phase_image_2, phase_image_1)
	#iSPMF = ifft2(SPOMF)
	
	r0 = np.abs(phase_image_1) * np.abs(phase_image_2)
	iSPMF = np.abs(ifft2((phase_image_1.conjugate() * phase_image_2) / r0))
	
	
	return iSPMF

##Image read in

##Currently Hard wired for something in my working directory as I have decided how best to loop this yet.
image1 = Image.open('scifestt.jpg')
image2 = Image.open('scifestt1.jpg')

data1 = np.array((image1))
data2 = np.array((image2))
#data2 = rotate(data2, 10, reshape = True, mode = 'nearest')

iSPMF1 = FMI(data1, data2)

try:
	rotation, scale = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
except:
	rotation, scale, colour = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
scaling_factor = np.exp(scale)
angle = 180.0 * rotation / iSPMF1.shape[0]
print(angle)
print(rotation)
print(scale)

try:
	n, m = (data2.shape/scaling_factor)
	n = int(n)
	m = int(m)
	scaled_image = np.resize(data2, (n,m))

	scaled_image_2 = scaled_image
	rot1 = rotate(scaled_image, rotation, reshape = True)
	rot2 = rotate(scaled_image_2, rotation+180, reshape = True)
	
except:
	n, m, colour = (data2.shape/scaling_factor)
	n = int(n)
	m = int(m)
	colour = int(colour)
	scaled_image = np.resize(data2, (n,m,colour))
	
	scaled_image_2 = scaled_image
	rot1 = rotate(scaled_image, rotation, axes=(0,1), reshape = False)
	rot2 = rotate(scaled_image_2, rotation+180, axes=(0,1), reshape = False)

iSPMF2 = FMI(data1, rot1)
iSPMF3 = FMI(data1, rot2)

A = np.amax(iSPMF2)
B = np.amax(iSPMF3)
