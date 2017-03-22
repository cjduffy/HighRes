import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift
from scipy.ndimage import rotate
import scipy.ndimage.interpolation as ndii 
import math
from scipy.signal import convolve2d

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
	square = np.lib.pad(image, ((diff_x,0), (diff_y,0)), 'constant', constant_values=(0,0))
	
	return square
	
def shaping(data1, data2):
	x1, y1 = data1.shape
	x2, y2 = data2.shape
	try:
		x = x2 - x1
		y = y2 - y1
		data1 = np.lib.pad(data1, ((x,0), (y,0) ), 'constant', constant_values=(0,0))
	except:
		x = x1 - x2
		y = y1 - y2
		data2 = np.lib.pad(data2, ((x,0), (y,0) ), 'constant', constant_values=(0,0))
	return data1, data2
	
def reshape(image_1, image_2):
	diff_x, diff_y = tuple(np.subtract(image_2.shape, image_1.shape))
	diff_x_arr = np.zeros(diff_x)
	diff_y_arr = np.zeros(diff_y)
	arrays = [diff_x_arr, diff_y_arr]
	n = m = k = l = 0
	counter_1 = [n,m]
	counter_2 = [k,l]
	stage = 0
	
	if diff_x % 2 == 1:
		range_end_one = int(math.ceil(diff_x/2))
	elif diff_x % 2 == 0:
		range_end_one = int(diff_x/2)
	
	if diff_y % 2 == 1:
		range_end_two = int(math.ceil(diff_y/2))
	elif diff_y % 2 == 0:
		range_end_two
		
	range_ends = [range_end_one, range_end_two]
	
	for stage in range(0,1):
		for counter_1[stage] in range(0, range_ends[stage]):
			arrays[stage] = np.insert(arrays[stage], counter_1[stage], counter_1[stage])
			counter_1[stage] += 1 
		for counter_2[stage] in range(1, range_ends[stage]):
			arrays[stage] = np.insert(arrays[stage], counter_2[stage]+counter_1[stage], image_2.shape[0]-counter_2[stage])
			counter_2[stage] += 1
		np.delete(image_2, arrays[stage], stage)
		stage += 1
	return(image_2)
