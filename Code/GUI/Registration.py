def _nd_window(data, filter_function):
	import numpy as np
	
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
	
def shaping(data1, data2):
	import numpy as np
	
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
	
def Logpolar(image, angles=None, radii=None):
	import scipy.ndimage.interpolation as ndii 
	import numpy as np
	import math
	
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

def correlation(image_1, image_2):
	from scipy.fftpack import fft2, ifft2, fftshift
	import numpy as np
	
	f0 = fft2(image_1)
	f1 = fft2(image_2)
	
	r0 = abs(f0) * abs(f1)
	iSPOMF = abs(ifft2((f0.conjugate() * f1) / r0))
	iSPOMF_shift = fftshift(iSPOMF)
	
	t0, t1 = np.unravel_index(np.argmax(iSPOMF_shift), iSPOMF_shift.shape)
	ret = np.array((t0, t1))
	
	t0 -= f0.shape[0] // 2
	t1 -= f0.shape[1] // 2
	
	ret -= np.array(f0.shape, int)//2
	
	return ret

def ang_scale(image_1, image_2):
	from scipy.fftpack import fft2, ifft2, fftshift
	import numpy as np
	
	shape = image_1.shape
	
	image_1 = fftshift(abs(fft2(image_1)))
	image_2 = fftshift(abs(fft2(image_2)))
	
	image_1 = _nd_window(image_1, np.hanning)
	image_2 = _nd_window(image_2, np.hanning)
	
	LP_image_1, logbase = Logpolar(image_1)
	LP_image_2, logbase = Logpolar(image_2)
	
	ang, scaling_factor = correlation(LP_image_1, LP_image_2)
	
	angle = -np.pi * ang
	angle = np.rad2deg(angle)
	scale = logbase ** scaling_factor
	angle = -1 *angle
	scale = 1/scale
	
	return angle, scale
		
def _get_emslices(shape1, shape2):
    """
    Common code used by :func:`embed_to` and :func:`undo_embed`
    """
    slices_from = []
    slices_to = []
    for dim1, dim2 in zip(shape1, shape2):
        diff = dim2 - dim1
        # In fact: if diff == 0:
        slice_from = slice(None)
        slice_to = slice(None)

        # dim2 is bigger => we will skip some of their pixels
        if diff > 0:
            # diff // 2 + rem == diff
            rem = diff - (diff // 2)
            slice_from = slice(diff // 2, dim2 - rem)
        if diff < 0:
            diff *= -1
            rem = diff - (diff // 2)
            slice_to = slice(diff // 2, dim1 - rem)
        slices_from.append(slice_from)
        slices_to.append(slice_to)
    return slices_from, slices_to
	
def embed_to(where, what):
	"""
	Given a source and destination arrays, put the source into
	the destination so it is centered and perform all necessary operations
	(cropping or aligning)

	Args:
		where: The destination array (also modified inplace)
		what: The source array

	Returns:
		The destination array
	"""
	slices_from, slices_to = _get_emslices(where.shape, what.shape)

	where[slices_to[0], slices_to[1]] = what[slices_from[0], slices_from[1]]
	return where

def transform_image(image, scale = 1.0, angle = 0.0, translation_vector = (0,0)):
	from scipy.ndimage import rotate
	import scipy.ndimage.interpolation as ndii
	import numpy as np
	
	bigshape = np.round(np.array(image.shape) * 1.2).astype(int)
				
	bg = np.zeros(bigshape, image.dtype)
	
	dest0 = embed_to(bg, image.copy())
	
	if scale != 1.0:
		dest0 = ndii.zoom(dest0, scale, order=1, mode='constant', cval=0)
	if angle != 0.0:
		dest0 = rotate(dest0, angle, reshape = False)
	if translation_vector[0] != 0 or translation_vector[1] != 0:
		dest0 = ndii.shift(dest0, translation_vector, mode='constant', cval=0)
	
	bg = np.zeros_like(image)
	dest = embed_to(bg, dest0)
	return dest
	
def check_rotation(image_1, image_2, image_3):
	from scipy.fftpack import fft2, ifft2, fftshift
	import numpy as np
	
	shape = image_1.shape
	
	image_1 = fftshift(abs(fft2(image_1)))
	image_2 = fftshift(abs(fft2(image_2)))
	image_3 = fftshift(abs(fft2(image_3)))
	
	image_1 = _nd_window(image_1, np.hanning)
	image_2 = _nd_window(image_2, np.hanning)
	image_3 = _nd_window(image_3, np.hanning)
	
	LP_image_1, logbase = Logpolar(image_1)
	LP_image_2, logbase = Logpolar(image_2)
	LP_image_3, logbase = Logpolar(image_3)
	
	f0 = fft2(LP_image_1)
	f1 = fft2(LP_image_2)
	f2 = fft2(LP_image_3)
	
	r0 = abs(f0) * abs(f1)
	iSPOMF1 = abs(ifft2((f0.conjugate() * f1) / r0))
	iSPOMF_shift1 = fftshift(iSPOMF1)
	
	r1 = abs(f0) * abs(f2)
	iSPOMF2 = abs(ifft2((f0.conjugate() * f2) / r1))
	iSPOMF_shift2 = fftshift(iSPOMF2)
	
	if np.amax(r0) > np.amax(r1):
		res = 0
	elif np.amax(r1) > np.amax(r0):
		res = 1
	else:
		print("Image appears to be identical under all rotations after scaling. Be aware that the results underr rotation may be imperfect.")
		res = 0
	
	return res
	
def translation(image_1, image_2):
	
	translation_difference = correlation(image_1, image_2)
	
	return translation_difference

def similarity(image_1, image_2):
		
	if image_1.shape != image_2.shape:
		image_1, image_2 = shaping(image_1, image_2)
		
	angle = 0.0
	scale = 1.0
	
	image_3 = image_2
	
	new_angle, new_scale = ang_scale(image_1, image_3)
	
	angle += new_angle
	scale *= new_scale
	image_3 = transform_image(image_2, scale, angle)
	image_3_180 = transform_image(image_2, scale, angle+180)

	check = check_rotation(image_1, image_3, image_3_180)
	
	if check == 0:
		del image_3_180
	if check == 1:
		image_3 =  image_3_180
		angle =+ 180
		del image_3_180
		
	translation_difference = translation(image_1, image_3)
	
	translation_vector = -1 * translation_difference
	
	dictionary = dict(translation_vector = translation_vector, angle =  angle, scale = scale)
	
	return dictionary
	
def stack(image_1, image_2):
	import numpy as np
	from astropy.io import fits
	
	image1 = fits.open(image_1)
	data1 = image1[0].data

	image2 = fits.open(image_2)
	data2 = image2[0].data
	
	if data1.ndim == 3:
		data1 = data1[:,:,0]
	if data2.ndim == 3:
		data2 = data2[:,:,0]
		
	data1 = np.nan_to_num(data1)
	data2 = np.nan_to_num(data2)
	
	dictionary = similarity(data1, data2)
	
	data3 = transform_image(data2, dictionary['scale'], dictionary['angle'], dictionary['translation_vector'])
	
	image_3 = abs(data1/2 + data3/2)
	
	return image_3
	
def for_colour_mapping(image_1, image_2):
	import numpy as np
	from astropy.io import fits
	
	image1 = fits.open(image_1)
	data1 = image1[0].data

	image2 = fits.open(image_2)
	data2 = image2[0].data
	
	if data1.ndim == 3:
		data1 = data1[:,:,0]
	if data2.ndim == 3:
		data2 = data2[:,:,0]
		
	data1 = np.nan_to_num(data1)
	data2 = np.nan_to_num(data2)
	
	dictionary = similarity(data1, data2)
	
	data3 = transform_image(data2, dictionary['scale'], dictionary['angle'], dictionary['translation_vector'])
	
	return data3

def Registration(folder):
	import os
	from astropy.io import fits
	import numpy as np
	
	filelist = []
	
	for file in os.listdir(folder):
		if file.endswith(".fits"):
			full_filepath = folder+"/"+file
			filelist.append(full_filepath)
			
	for file in os.listdir(folder):
		if folder+"/"+file == filelist[0]:
			stacked_image = fits.open(filelist[0])
			stacked_image = stacked_image[0].data
			if stacked_image.ndim == 3:
				stacked_image = stacked_image[:,:,0]
			stacked_image = np.zeros_like(stacked_image, dtype = float)
			pass
		else:
			stacked_image += stack(filelist[0], folder+"/"+file)
	
	n = 1
	filename = "Stacked_Image_"+str(n)+".fits"
	
	while True:
		if os.path.isfile(folder+"/"+filename):
			n += 1
			filename = "/Stacked_Image_"+str(n)+".fits"
		else:
			break
			
	hdu = fits.PrimaryHDU()
	hdu.data = stacked_image
	hdu.writeto(folder+"/"+filename, overwrite = False)
	
	return(0)
	
def colour_mapping(image_1, image_2, number):
	from PIL import Image
	import matplotlib
	import matplotlib.pyplot as plt
	import os
	 
	image_2 = for_colour_mapping(image_1, image_2)
	 
	image_2_image = Image.fromarray(image_2)
	plt.imsave("temp.tif", image_2_image, cmap="Created Space "+str(number), format="tif")
	image_2_new = Image.open("temp.tif")
	
	blended = Image.blend(image_1, image_2, alpha = 0.5)
	os.remove("temp.tif")
	
	return blended

def Layering(list_of_images):
	import os
	from astropy.io import fits
	
	filelist = list_of_images
	x = 0
	stacked_image = np.array((1,1))
	
	for x in range(0, len(filelist)):
		if x == 0:
			pass
		else:
			stacked_image += colour_mapping(filelist[0], filelist[x], x)
			
	n = 1
	filename = "Stacked_Image_"+str(n)+".fits"
	
	while True:
		if os.path.isfile(folder+"/"+filename):
			n += 1
			filename = "/Stacked_Image_"+str(n)+".fits"
		else:
			break
			
	hdu = fits.PrimaryHDU()
	hdu.data = stacked_image
	hdu.writeto(folder+"/"+filename, overwrite = False)
