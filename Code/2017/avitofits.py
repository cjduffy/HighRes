#Frame Capture to FITS
#Written by Mick Wright and Chris Duffy

#Script examines current working directory for all .avi files, goes through them frame by frame and creates first a TIF, and then a FITS file. 

###Future Plans: Convert to function for GUI, and create a switch for keeping the TIFs or removing them. 

#Necessary imports and name changes for ease of use
import os
import numpy as np
from astropy.io import fits
from PIL import Image
import cv2

#get current working directory
cwd = os.getcwd()
#begin counter
n=1

#for loop examines all files in the current working directory, selecting those whose file extensions end in .avi and splits the avi into individual frames, saving them as TIFs, and then converting them into FITS
for file in os.listdir(cwd):
	if file.endswith(".avi"):
		video_capture = cv2.VideoCapture(file)
		
		while True:
			#check frame is there, and read it in
			ret, frame = video_capture.read()
			#if at end of video, break out of loop
			if (ret != True):
				break
			
			#construct the filenames
			filename_tif = "frame_%d.tif" %n
			filename_fits = "frame_%d.fits" %n
			
			#write the TIF
			cv2.imwrite(filename_tif,frame)
			
			#convert to FITS and remove TIF
			hdu = fits.PrimaryHDU()
			im = Image.Open(filename_tif)
			hdu.data = np_array(im)
			hdu.writeto(filename_fits, overwrite = True)
			os.remove(filename_tif)
			
			#increment counter
			n = n+1
			
#release the video at the end
video_capture.release()

