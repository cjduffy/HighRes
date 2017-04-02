def avi_to_fits(data_list, data_type, switch=False):
	
	import os
	import numpy as np
	import cv2
	from astropy.io import fits
	from PIL import Image
	
	l = 1
	
	if data_list[data_type].data_mode == "single":
		n = 1
		if data_list[data_type].data.endswith(".avi"):
			full_filepath = data_list[data_type].data
			filepath = os.path.dirname(os.path.realpath(full_filepath))
			actual_file = os.path.basename(full_filepath)
			video_capture = cv2.VideoCapture(full_filepath)
			
			filename = actual_file.replace(".avi", "")
			folder = filepath+"/"+filename
			
			if not os.path.exists(folder):
				os.mkdir(folder)
				
			Imtype = data_list[data_type].data_type
			if Imtype == "raw":
				Imtype = "frame"
			
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
			
	elif data_list[data_type].data_mode == "group":
		for file in os.listdir(data_list[data_type].data):
			n = 1
			if file.endswith(".avi"):
				filepath = data_list[data_type].data+"/"+file
				video_capture = cv2.VideoCapture(filepath)
				
				folder = filepath.replace(".avi", "")
				
				if not os.path.isdir(folder):
						os.mkdir(folder)
						
				Imtype = data_list[data_type].data_type
				if Imtype == "raw":
					Imtype = "frame"
						
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

	
