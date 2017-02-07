import numpy as np
from scipy.signal import convolve2d
from astropy.io import fits


Image = fits.open('FILE')
arr = Image[0].data

x = np.matrix('0 1 0; 1 0 1; 0 1 0')
y = np.divide(x, 4)

print(x)

mean = convolve2d(arr,y, mode='same')

arr[arr > 2000] = mean[arr > 2000]

#MUST INTEGRATE SOME METHOD OF SELECTING THE THRESHOLD FROM THE AVERAGE DARK CURRENT
