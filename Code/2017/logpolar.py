def logpolar(image):
	
	import numpy as np
	import math
	
	##Initialise X Counter
	x = 1
	
	##Get Shape of Image
	max_x, max_y = Image.shape
	Log_Polar_Image = np.zeros((max_x, max_y))
	
	##Calculate the centre position
	center_x = max_x/2
	center_y = max_y/2
	
	##Loop Through x and y:
	for x in range(1,max_x):
		y = 1
		for y in range(1,max_y):
			x_pos = x - center_x
			y_pos = y - center_y
			
			r = math.sqrt(x_pos**2 + y_pos**2)
			a_in = math.fabs(y_pos/x_pos)
			a = math.arctan(a_in)
			ep = math.log10(r)
			
			Log_Polar_Image[ep,a] = Image[x,y]
			
	return(Log_Polar_Image)
	

			
			
			
