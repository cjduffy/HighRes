function [ Processed_Images ] = ProcessParOne(Image) 
%%Image Processing Part One- as laid out in 'Processing RAW images in
%%MATLAB. Code Credit goes to paper author, Rob Sumner

%%Linearising Information - image linearised by dcraw
%raw = double(imread(Image));
black = 2048;
saturation = 13584;
lin_bayer = (Image-black)/(saturation-black);
lin_bayer = max(0,min(lin_bayer,1));

%%White Balancing
wb_multipliers  = [1.935457 1, 1.667969];
mask = wbmask(size(lin_bayer,1),size(lin_bayer,2),wb_multipliers,'rggb');
balanced_bayer = lin_bayer.*mask; 

Processed_Images = balanced_bayer; 

end 