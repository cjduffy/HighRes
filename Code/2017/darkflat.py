#  darkflat.py
#  
#  Copyright 2017 Chris Duffy
#  
#  Currently this program of taking a file
#  programed into it and running a dark
#  current and flat field correction process
# using preexisting dark and flat fields..
#  
#  Program will need updated to operate
#  as a fucntion and may need some file
#  pointers changed as approriate.
#  
#  


import os
from astropy.io import fits
import numpy as np


Image = fits.open(FILE_NAME)
imagedata = Image[0].data


##Checking the existance of Flat Field and Dark Current Images and reads them in
if os.path.isfile('Master Flat.fits'):
	flat_field = fits.open('Master Flat.fits') 
	flatdata = flat_field[0].data
elif os.path.isfile('FF.fits'):
	flat_field = fits.open('FF.fits')
	flatdata = flat_field[0].data
else:
	print('Error:No Flat Field')
	#Add Error Condiditon Here
	
if os.path.isfile('Master Dark.fits'):
	Dark_Current = fits.open('Master Dark.fits')
	darkdata = Dark_Current[0].data
elif os.path.isfile('DC.fits'):
	Dark_Current = fits.open('DC.fits')
	darkdata = Dark_Current[0].data
else:
		print('Error:No Dark Current')
		#Add Error Condition Here
		
##Performs Dark/Flat corrections
Dark_Removed = np.subtract(imagedata, darkdata)
Corrected_Image = np.divide(Dark_Removed, flatdata)
