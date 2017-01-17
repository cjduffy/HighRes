clear
A = imread('IMG_3761.CR2'); %reading in the dark current
B = imread('IMG_3799.CR2'); %reading in im171
C = imread('20160216_151135.CR2'); %reading in flatfield
E=B-A;
mean_value=mean(E(:)); %calculating the mean value of the dark field

%E = B-mean_value; %image corrected by removal of average dark current
%F = C-mean_value; %image corrected by removal of average dark current
%F= E./C;

D=((E)*mean_value)/(C-A);

imwrite(D,'test1.tif', 'tif') 

[w,x] = hist(E(:)); %records variables of histogram
%[y,z] = hist(F(:),300);

W = log10(w); %takes log10 of the counts
%Y = log10(y);

subplot(2,1,1) %plots the corrected histograms
bar(x,W)
title('17.1nm Image Counts')
subplot(2,1,2)
%bar(z,Y)
%title('19.5 nm Image Counts')
%bar charts show cut off between imaged photons and hot pixels use these in
%script 8b
%clear ('A', 'B', 'C','w', 'x', 'y', 'z', 'W', 'Y', 'mean_value')
