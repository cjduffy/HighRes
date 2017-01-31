import os
import cv2
cwd = os.getcwd()
n = 1

for file in os.listdir(cwd):
	if file.endswith(".avi"):
		video_capture = cv2.VideoCapture(file)
		
		while True:
			ret, frame = video_capture.read()
			filename = 'frame_%d.tif' %n
			cv2.imwrite(filename,frame)
			n = n+1
			print(filename)
