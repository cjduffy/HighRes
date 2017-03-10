import numpy as np
from scipy.fftpack import fft2, ifft2
from scipy.ndimage import rotate
import scipy.ndimage.interpolation as ndii 
import math
#Final version won't need PIL
from PIL import Image

def logpolar(image, angles=None, radii=None):
    shape = image.shape
    center = shape[0] / 2, shape[1] / 2
    if angles is None:
        angles = shape[0]
    if radii is None:
        radii = shape[1]
    theta = np.empty((angles, radii), dtype=np.float64)
    theta.T[:] = -np.linspace(0, np.pi, angles, endpoint=False)
    #d = radii
    d = np.hypot(shape[0]-center[0], shape[1]-center[1])
    log_base = 10.0 ** (math.log10(d) / (radii))
    radius = np.empty_like(theta)
    radius[:] = np.power(log_base, np.arange(radii,
                                                   dtype=np.float64)) - 1.0
    x = radius * np.sin(theta) + center[0]
    y = radius * np.cos(theta) + center[1]
    output = np.empty_like(x)
    ndii.map_coordinates(image, [x, y], output=output)
    return output, log_base

##Image read in

##Currently Hard wired for something in my working directory as I have decided how best to loop this yet.
image1 = Image.open('outfile.jpg')
image2 = Image.open('outfile2.jpg')

data1 = np.array(image1)
data2 = np.array(image2)

def FMI(data1, data2):
	
	LP1, log_base = logpolar(data1)
	LP2, log_base = logpolar(data2)
	
	##Fourier Time!
	
	transform_image_1 = fft2(LP1)
	transform_image_2 = fft2(LP2)
	
	phase_image_1 = np.imag(transform_image_1)
	phase_image_2 = np.imag(transform_image_2)
	
		
	if phase_image_1.shape != phase_image_2.shape:
		x2, y2 = phase_image_2.shape
		x1, y1 = phase_image_1.shape
		x = x2 - x1
		y = y2 - y1
		phase_image_1 = np.lib.pad(phase_image_1, ((x,0), (y,0)), 'edge')
		
	
	SPOMF = np.subtract(phase_image_2, phase_image_1)
	iSPMF = ifft2(SPOMF)

	return iSPMF
	
iSPMF1 = FMI(data1, data2)

rotation, scale = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
scaling_factor = np.exp(scale)
n, m = (data2.shape/scaling_factor)
n = int(n)
m = int(m)

##The size of the array must be cast to an array.
##If the array is recaled by too much it won't work.

scaled_image = np.resize(data2, (m,n))
scaled_image_2 = scaled_image

rot1 = rotate(scaled_image, rotation)
rot2 = rotate(scaled_image_2, rotation+180)

iSPMF2 = FMI(data1, rot1)
iSPMF3 = FMI(data1, rot2)

rotation1, scale1 = np.unravel_index(np.argmax(iSPMF2), iSPMF2.shape)
rotation2, scale2 = np.unravel_index(np.argmax(iSPMF3), iSPMF3.shape)
