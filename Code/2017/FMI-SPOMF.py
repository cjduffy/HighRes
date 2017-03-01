import cv2
import numpy as np
from scipy.fftpack import fft2, ifft2

##Image read in

##Convert to logpolar

LP1 = cv2.logPolar(image1)
LP2 = cv2.logPolar(image2)

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
 

