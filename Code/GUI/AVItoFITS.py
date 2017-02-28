def avi_to_fits(single="none", group="none", switch=False, Imtype="frame"):
	
	import os
	import numpy as np
	import cv2
	from astropy.io import fits
	from PIL import Image
	
	l = 1
	
	if (single != "none"):
		for file in os.listdir(os.path.dirname(os.path.realpath(single))):
			if file.startswith(str(Imtype)+"_"+str(l)):
				l = l + 1 
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
				filepath = os.path.dirname(os.path.realpath(single))
				filename_tif = filepath+"/"+single+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".tif"
				filename_fits = filepath+"/"+single+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".fits"
			
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
		else:
			return(100)
			
	elif (group != "none"):
		for file in os.listdir(group):
			if file.startswith(str(Imtype)+"_"+str(l)):
				l = l + 1
				
		for file in os.listdir(group):
			n = 1
			if file.endswith(".avi"):
				filepath = group+"/"+file
				video_capture = cv2.VideoCapture(filepath)
				while True:
			#check frame is there, and read it in
					ret, frame = video_capture.read()
			#if at end of video, break out of loop
					if (ret != True):
						break
						
			
			#construct the filenames
					filename_tif = group+"/"+file+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".tif"
					filename_fits = group+"/"+file+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".fits"
			
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
	else:
		return (200)
		
	return(1) 
