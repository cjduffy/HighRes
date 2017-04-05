def avi_to_fits(data_list_entry):
	
	import os
	from astropy.io import fits
	import numpy as np
	import cv2
	from PIL import Image
	
	l = 1
	
	if data_list_entry.data_mode == "single":
		n = 1
		if data_list_entry.data_filedata.endswith(".avi"):
			filepath = os.path.dirname(os.path.realpath(data_list_entry.data_filedata))
			actual_file = os.path.basename(data_list_entry.data_filedata)
			video_capture = cv2.VideoCapture(data_list_entry.data_filedata)
			
			filename = actual_file.replace(".avi", "")
			folder = filepath+"/"+filename
			
			if not os.path.exists(folder):
				os.mkdir(folder)
				
			if data_list_entry.data_type == "raw":
				imtype = "frame"
			else:
				imtype = data_list_entry.data_type
				
			while True:
				filename_initial = folder+"/"+str(imtype)+"_"+str(l)+"_"+str(n)+".fits"
				if os.path.isfile(filename_initial):
					l = l + 1
				else:
					break
					
			while True:
				ret, frame = video_capture.read()
				if (ret != True):
					break
				
				filename_tif = folder+"/"+str(imtype)+"_"+str(l)+"_"+str(n)+".tif"
				filename_fits = filename_tif.replace(".tif", ".fits")
				
				cv2.imwrite(filename_tif, frame)
				
				hdu = fits.PrimaryHDU()
				im = Image.open(filename_tif)
				hdu.data = np.array(im)
				hdu.writeto(filename_fits, overwrite=True)
				
				if data_list_entry.state == False: 
					os.remove(filename_tif)
					
				n += 1
		else:
			wrn_dialog = Gtk.Dialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "File not AVI")
			wrn_dialog.format_secondary_text("The selected file is not an avi and cannot be split into FITS")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
		
	elif data_list_entry.data_mode == "group":
		for file in os.listdir(data_list_entry.data_filedata):
			n = 1
			
			if file.endswith(".avi"):
				filepath = data_list_entry.data_filedata
				actual_file = data_list_entry.data_filedata+"/"+file
				video_capture = cv2.VideoCapture(actual_file)
				
				filename = file.replace(".avi", "")
				folder = filepath+"/"+filename
				
				if not os.path.exists(folder):
					os.mkdir(folder)
					
				if data_list_entry.data_type == "raw":
					imtype = "frame"
				else:
					imtype = data_list_entry.data_type
					
				while True:
					filename_initial = folder+"/"+str(imtype)+"_"+str(l)+"_"+str(n)+".fits"
					if os.path.isfile(filename_initial):
						l = l + 1
					else:
						break
						
				while True:
					ret, frame = video_capture.read()
					if (ret != True):
						break
					
					filename_tif = folder+"/"+str(imtype)+"_"+str(l)+"_"+str(n)+".tif"
					filename_fits = filename_tif.replace(".tif", ".fits")
					
					cv2.imwrite(filename_tif, frame)
					
					hdu = fits.PrimaryHDU()
					im = Image.open(filename_tif)
					hdu.data = np.array(im)
					hdu.writeto(filename_fits, overwrite=True)
					
					if data_list_entry.state == False: 
						os.remove(filename_tif)
						
					n += 1
				l += 1
				
			else:
				pass
				
	else:
		print("Data mode error")
		return(2)
		
	return(0)
			
	

	
