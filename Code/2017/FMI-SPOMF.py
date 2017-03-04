import cv2
import numpy as np
from scipy.fftpack import fft2, ifft2
from scipy.ndimage import rotate
#Final version won't need PIL
from PIL import Image

##Image read in

##Currently Hard wired for something in my working directory as I have decided how best to loop this yet.
image1 = Image.open('outfile.jpg')
image2 = Image.open('outfile.jpg')

data1 = np.array(image1)
data2 = np.array(image2)


center1 = np.divide((data1.size), 2)
center2 = np.divide((image2.size), 2)

##Convert to logpolar
##There is something wrong here, the documentatoin is non existant, I might actually be foreced to ask stackoverflow
##Might just be best to write out the maths of this manuaually using formula laid out by wikipedia.
LP1 = cv2.logPolar(data1, center1, 0.1,[cv2.WARP_FILL_OUTLIERS, 1])
LP2 = cv2.logPolar(data2, center2, 10, [cv2.WARP_FILL_OUTLIERS, 1])

##Fourier Time!

transform_image_1 = fft2(LP1)
transform_image_2 = fft2(LP2)

phase_image_1 = np.imag(transform_image_1)
phase_image_2 = np.imag(transform_image_2)

SPOMF = np.subtract(phase_image_2, phase_image_1)
iSPMF = ifft2(SPOMF)

rotation, scale = np.unravel_index(np.argmax(iSPMF), iSPMF.shape)
scaling_factor = np.exp(scale)

scaled_image = np.divide(image2, scaling_factor)
scaled_image_2 = scaled_image

rot1 = rotate(scaled_image, rotation)
rot2 = rotate(scaled_image_2, rotation+180)

