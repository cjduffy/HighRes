import os
import cv2
from astropy.io import fits
import numpy as np
from PIL import Image

cwd = os.getcwd()
n=1

for file in os.listdir(cwd):
	if file.endswith(".avi"):
		video_capture = cv2.VideoCapture(file)
		
		while True:
			ret, frame = video_capture.read()
			filename_tif = 'frame_%d.tif' %n
			cv2.imwrite(filename_tif,frame)
			
			hdu = fits.PrimaryHDU()
		
			im = Image.open('frame_%d.tif' %n)
			hdu.data = np.array(im)
			filename_fits = 'frame_%d.fits' %n				
			hdu.writeto(filename_fits, overwrite=True)
		
			os.remove(filename_tif)
			n = n+1
			
		
			
	
