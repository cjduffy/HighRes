import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift
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
    
def Logpolar(image, angles=None, radii=None):
    """Return log-polar transformed image and log base."""
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
    radius[:] = np.power(log_base, np.arange(radii, dtype=np.float64)) - 1.0
    x = radius * np.sin(theta) + center[0]
    y = radius * np.cos(theta) + center[1]
    output = np.empty_like(x)
    output = ndii.map_coordinates(image, [x, y])
    return output, log_base
    
def makeSquare(image):
	if image.shape[0] <= image.shape[1]:
		diff_x = image.shape[1] - image.shape[0]
	else:
		diff_x = 0
	if image.shape[1] <= image.shape[0]:
		diff_y = image.shape[0] - image.shape[1]
	else:
		diff_y = 0	
	square = np.lib.pad(image, ((diff_x,0), (diff_y,0)), 'edge')
	return square
	
def shaping(data1, data2):
	x1, y1 = data1.shape
	x2, y2 = data2.shape
	try:
		x = x2 - x1
		y = y2 - y1
		data1 = np.lib.pad(data1, ((x,0), (y,0) ), 'edge')
	except:
		x = x1 - x2
		y = y1 - y2
		data2 = np.lib.pad(data2, ((x,0), (y,0) ), 'edge')
	return data1, data2

def FMI(data1, data2, polar):
	if data1.shape[0] != data1.shape[1]:
		data1 = makeSquare(data1)	
	if data2.shape[0] != data2.shape[1]:
		data2 = makeSquare(data2)
	
	if data1.shape != data2.shape:
		data1, data2 = shaping(data1, data2)
	if polar is False:
		data1 = fftshift(abs(fft2(data1)))
		data2 = fftshift(abs(fft2(data2)))
	
		data1_W = _nd_window(data1, np.hanning)
		data2_W = _nd_window(data2, np.hanning)

	
		LP1, logbase = Logpolar(data1_W)
		LP2, logbase = Logpolar(data2_W)
	else:
		LP1 = data1
		LP2 = data2
		
	phase_image_1 = fft2(LP1)
	phase_image_2 = fft2(LP2)

	#SPOMF = np.multiply(phase_image_2, phase_image_1)
	#iSPMF = ifft2(SPOMF)
	
	r0 = abs(phase_image_1) * abs(phase_image_2)
	iSPMF = abs(ifft2((phase_image_1.conjugate() * phase_image_2) / r0))
	
	
	return iSPMF

##Image read in

##Currently Hard wired for something in my working directory as I have decided how best to loop this yet.
image1 = Image.open('outfile.jpg')
image2 = Image.open('outfile.jpg')

data1 = np.array((image1))
data2 = np.array((image2))

if data1.ndim == 3:
	data1 = data1[:,:,0]
if data2.ndim == 3:
	data2 = data2[:,:,0]
data2 = rotate(data2, 180, reshape = False)

iSPMF1 = FMI(data1, data2, False)

rotation, scale = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
scaling_factor = np.exp(scale)
angle = 180.0 * rotation / iSPMF1.shape[0]


if scaling_factor > 1.8:
	angle = -1 * angle
	scaling_factor = 1.0 / scaling_factor
	print(scaling_factor)
	if scale > 1.8:
		raise ValueError("You broke it, the scale differnce was too large") #GTK waning probably better here also
print(angle)
print(scaling_factor)

n, m = (data2.shape/scaling_factor)
n = int(n)
m = int(m)
scaled_image = np.resize(data2, (n,m))

scaled_image_2 = scaled_image
rot1 = rotate(scaled_image, angle, reshape = False)
rot2 = rotate(scaled_image_2, angle+180, reshape = False)
	

iSPMF2 = FMI(data1, rot1, True)
iSPMF3 = FMI(data1, rot2, True)

A = np.amax(iSPMF2)
B = np.amax(iSPMF3)
print(A)
print(B)
A=B
if A > B:
	print("Do your thing with iSPMF2")
elif B > A:
	print("Do your thing with iSPMF3")
else:
	print("Image appears identical under all roations after scaling, attempting to proceed but results may be imperfect")
	#Probably worth calling either a GTK wanring window if this condition is met or a terminal wanring but I am too tired to work out the latter and the former is not my skill set.
