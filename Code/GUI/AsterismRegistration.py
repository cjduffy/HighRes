import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift
from scipy.ndimage import rotate
import scipy.ndimage.interpolation as ndii 
import math
from scipy.signal import convolve2d
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
	x, y = image_2.shape
	
	if diff_x % 2 == 1:
		x_limits = int(math.ceil(diff_x/2))
	else:
		x_limits = int(diff_x/2)
	
	if diff_y % 2 == 1:
		y_limits = int(math.ceil(diff_y/2))
	else:
		y_limits = int(diff_y/2)
		
	new_size_x = x - diff_x
	new_size_y = y - diff_y 
	
	image_2_corrected = np.zeros((new_size_x, new_size_y))
	print(image_2_corrected.shape)
	
	start_position_x = x_limits
	end_position_x = x - x_limits
	print(end_position_x - start_position_x)
	
	start_position_y = y_limits
	end_position_y = y - y_limits
	print(end_position_y - start_position_y)
	
	y_count = start_position_y
	x_count = start_position_x
	n = 0
	m = 0
	
	for y_count in range(start_position_y, end_position_y):
		x_count = start_position_x
		n = 0
		for x_count in range(start_position_x, end_position_x):
			image_2_corrected[n,m] = image_2[x_count, y_count]
			n += 1
			x_count += 1
		m += 1
		y_count += 1
		
		
	return(image_2_corrected)
	
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
	
	r0 = abs(phase_image_1) * abs(phase_image_2)
	iSPMF = abs(ifft2((phase_image_1.conjugate() * phase_image_2) / r0))
	
	
	return iSPMF

def registration(data1, data2):

	if data1.ndim == 3:
		data1 = data1[:,:,0]
	if data2.ndim == 3:
		data2 = data2[:,:,0]

	iSPMF1 = FMI(data1, data2, False)

	rotation, scale = np.unravel_index(np.argmax(iSPMF1), iSPMF1.shape)
	scaling_factor = np.exp(scale)
	angle = 180.0 * rotation / iSPMF1.shape[0]

	if scaling_factor > 1.8:
		angle = -1 * angle
		scaling_factor = 1.0 / scaling_factor
		if scale > 1.8:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Breached Scaling Height")
			wrn_dialog.format_secondary_text("Scaling factor too large to proceed.")
			wrn_dialog.run()
			wrn_dialog.destroy
			return("Scaling Factor Too Large")

	n, m = (data2.shape/scaling_factor)
	n = int(n)
	m = int(m)
	scaled_image = np.resize(data2, (n,m))

	scaled_image_2 = scaled_image
	rot1 = rotate(scaled_image, -1 * angle, reshape = False)
	rot2 = rotate(scaled_image_2, -1* (angle+180), reshape = False)
	
	iSPMF2 = FMI(data1, rot1, True)
	iSPMF3 = FMI(data1, rot2, True)

	A = np.amax(iSPMF2)
	B = np.amax(iSPMF3)

	if A > B:
		corrected_rotation = reshape(data1, rot1)

	elif B > A:
		corrected_rotation = reshape(data1, rot2)
	
	else:
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Rotational Equality Detected")
		dialog.format_secondary_text("Image appears to be identical under all rotations after scaling, process will proceed upon pressing the OK button. Be warned that the results may be imperfect.")
		dialog.run()
		dialog.destroy()
		corrected_rotation = reshape(data1, rot1)
	
	f0 = fft2(data1)
	f1 = fft2(corrected_rotation)
	iSPMF4 = abs(ifft2((f0 * f1.conjugate()) / (abs(f0) * abs(f1))))
	t0, t1 = np.unravel_index(np.argmax(iSPMF4), iSPMF4.shape)

	if t0 > f0.shape[0] // 2:
		t0 -= f0.shape[0]
	if t1 > f0.shape[1] // 2:
		t1 -= f0.shape[1]
		
	corrected_image = ndii.shift(corrected_rotation, [t0, t1])
	return corrected_image
	
def imshow(im0, im1, im2, im3= None, cmap=None, **kwargs):
	"""Plot images using matplotlib."""
	from matplotlib import pyplot
	if cmap is None:
		cmap = 'rainbow'
	if im3 is None:
		im3 = abs(im2/2 + im0/2)
	pyplot.subplot(221)
	pyplot.imshow(im0, cmap, **kwargs)
	pyplot.subplot(222)
	pyplot.imshow(im1, cmap, **kwargs)
	pyplot.subplot(223)
	pyplot.imshow(im3, cmap, **kwargs)
	pyplot.subplot(224)
	pyplot.imshow(im2, cmap, **kwargs)
	pyplot.show()

##Image read in

##Currently Hard wired for something in my working directory as I have decided how best to loop this yet.
image1 = Image.open('scifestt.jpg')
image2 = Image.open('scifestt.jpg')
data1 = np.array((image1))
data2 = np.array((image2))
data2 = rotate(data2, 215, reshape = True)
corrected_image = registration(data1, data2)

if data1.ndim == 3:
	data1 = data1[:,:,0]
imshow(data1, data2, corrected_image)
