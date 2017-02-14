import numpy as np
import os
from astropy.io import fits

cwd = os.getcwd()
time = 1
dark_time = 1
n = 1
m = 1
k = 1

#Use integration times 5 times the length of the longest integration

flat = fits.open('flat_1.fits')
flatdata = flat[0].data
size = flatdata.shape
flat = np.zeros(size)

flatCounter = 0
for root, dirs, files in os.walk(cwd):
    for file in files:    
        if file.startswith('flat_'):
            flatCounter += 1

for file in os.listdir(cwd)
	for n in range (1, flatCounter)
		flat_field = "flat_%d" %n
		flat_fit = fits.open(flat_field)
		flatdata = flat_fit[0].data
		flat = np.add(flat, flatdata)
	
		n += 1

mean_flat = np.divide(flats, n)
mean_flat_dark = np.divide(flat_darks, n)
master_flat = np.subtract(mean_flat, mean_flat_dark)

bias = fits.open('bias_1.fits')
biasdata = flat[0].data
size = biasdata.shape
bias = np.zeros(size)

biasCounter = 0
for root, dirs, files in os.walk(cwd):
    for file in files:    
        if file.startswith('bias_'):
            biasCounter += 1
            
for file in os.listdir(cwd)
	for n in range (1, biasCounter)
		bias_name = "bias_%d" %m
		bias_fit = fits.open(bias_name)
		biasdata = bias_fit[0].data
		bias = np.add(bias, biasdata)
	
		m += 1

mean_bias = np.divide(bias, m)

dark = fits.open('dark_1.fits')
darkdata = dark[0].data
size = darkdata.shape
dark = np.zeros(size)

darkCounter = 0
for root, dirs, files in os.walk(cwd):
    for file in files:    
        if file.startswith('dark_'):
            darkCounter += 1
            
for file in os.listdir(cwd)
	for n in range (1, darkCounter)
		dark_name = "dark_%d" %k
		dark_fit = fits.open(dark_name)
		darkdata = dark_fit[0].data
		dark = np.add(dark, dakrdata)
	
		k += 1

mean_dark = np.divide(darks, k)
thermal = np.subtract(mean_dark, mean_bias)
scaling_ratio = np.divide(time, dark_time)
scaled_thermal = np.multiply(scaling_ratio, thermal)

hdu = fits.PrimaryHDU()
hdu.data = master_flat
hdu.writeto('Master Flat.fits', overwrite = True)

hdu = fits.PrimaryHDU()
hdu.data = master_flat
hdu.writeto('Master Flat.fits', overwrite = True)
