image = imread('Images/Lenna.png');
image = image(:,:,1);
n = 1;
for d = 0.01:0.005:0.1
    salt = pepperOrSalt(image,d,2,0,255);
    filename = sprintf('salt_%d.fits', n);
    fitswrite(salt, filename)
    n = n+1;
end 
