def avi_to_fits(single="none", group="none", switch=False, Imtype="frame"):
	
	import os
	import numpy as np
	import cv2
	from astropy.io import fits
	from PIL import Image
	
	l = 1
	
	if (single != "none"):
		n = 1
		if single.endswith(".avi"):
			filepath = os.path.dirname(os.path.realpath(single))
			actual_file = os.path.basename(single)
			video_capture = cv2.VideoCapture(single)
			
			filename = actual_file.replace(".avi", "")
			folder = filepath+"/"+filename
			
			if not os.path.exists(folder):
				os.mkdir(folder)
				
			while True:	
				filename_initial = folder+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".fits"
				if os.path.isfile(filename_initial):
					l = l + 1
				else:
					break
	
			while True:
				ret, frame = video_capture.read()
				if (ret != True):
					break
					
				filename_tif = folder+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".tif"
				filename_fits = folder+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".fits"
			
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
			n = 1
			if file.endswith(".avi"):
				filepath = group+"/"+file
				video_capture = cv2.VideoCapture(filepath)
				
				folder = filepath.replace(".avi", "")
				
				if not os.path.isdir(folder):
						os.mkdir(folder)
						
				while True:	
						filename_initial = folder+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".fits"
						if os.path.isfile(filename_initial):
							l = l + 1
						else:
							break
				
				while True:
					ret, frame = video_capture.read()
					if (ret != True):
						break
					
					filename_tif = folder+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".tif"
					filename_fits = folder+"/"+str(Imtype)+"_"+str(l)+"_"+str(n)+".fits"
						
					cv2.imwrite(filename_tif,frame)
				
					hdu = fits.PrimaryHDU()
					im = Image.open(filename_tif)
					hdu.data = np.array(im)
					hdu.writeto(filename_fits, overwrite = True)
					if switch != True: 
						os.remove(filename_tif)
					n = n+1
				l = l+1
			else:
				pass
	else:
		return (200)
		
	return(1) 
