image = imread('Lenna.png');
image = image(:,:,1);
n = 1;
for d = 0.01:0.005:0.1
    salt_pepper = imnoise(image,'salt & pepper', d);
    filename = sprintf('salt_pepper_%d.fits', n);
    fitswrite(salt_pepper, filename)
    n = n+1;
end 
