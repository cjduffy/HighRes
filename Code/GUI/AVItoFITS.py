def avi_to_fits(single="none", group="none", switch=False):
	
	import os
	import numpy as np
	import cv2
	from astropy.io import fits
	from PIL import Image
	
	if (single != "none"):
		n = 1
		if single.endswith(".avi"):
			video_capture = cv2.VideoCapture(single)
		
			while True:
			#check frame is there, and read it in
				ret, frame = video_capture.read()
			#if at end of video, break out of loop
				if (ret != True):
					break
			
			#construct the filenames
				filepath = single
				filename_tif = single+"frame_%d.tif" %n
				filename_fits = single+"frame_%d.fits" %n
			
			#write the TIF
				cv2.imwrite(filename_tif,frame)
			
			#convert to FITS and remove TIF
				hdu = fits.PrimaryHDU()
				im = Image.open(filename_tif)
				hdu.data = np.array(im)
				hdu.writeto(filename_fits, overwrite = True)
				if switch != True: 
					os.remove(filename_tif)
			
			#increment counter
				n = n+1
			return(1)
		else:
			return(100)
			
	elif (group != "none"):
		l = 1
		for file in os.listdir(group):
			n = 1
			if file.endswith(".avi"):
				video_capture = cv2.VideoCapture(file)
				while True:
			#check frame is there, and read it in
					ret, frame = video_capture.read()
			#if at end of video, break out of loop
					if (ret != True):
						break
						
			
			#construct the filenames
					filename_tif = group+"/frame_"+str(l)+"_"+str(n)+".tif"
					filename_fits = group+"/frame_"+str(l)+"_"+str(n)+".fits"
			
			#write the TIF
					cv2.imwrite(filename_tif,frame)
			
			#convert to FITS and remove TIF
					hdu = fits.PrimaryHDU()
					im = Image.open(filename_tif)
					hdu.data = np.array(im)
					hdu.writeto(filename_fits, overwrite = True)
					if switch != True: 
						os.remove(filename_tif)
			
			#increment counter
					n = n+1
				l = l+1
			else:
				pass
		return(2)
	else:
		return (200)
			
	
