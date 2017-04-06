image = imread('Lenna.png');
n = 1;
for x = 1:2:50
    blurred = imgaussfilt(image, n);
    filename = sprintf('blurred_%d.png', n);
    imwrite(blurred, filename)
    n = n+1;
end 
