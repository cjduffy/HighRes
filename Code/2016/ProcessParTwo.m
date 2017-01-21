function [ final_image ] = ProcessParTwo( balanced_bayer )
%%Image Processing Part 2 - as laid out in the paper 'Processing Raw Images
%%in Matlab'. Code credit goes to the paper author, Rob Sumner. 

%%Demosaicing
temp = uint16(balanced_bayer/max(balanced_bayer(:))*2^16);
lin_rgb = double(demosaic(temp,'rggb'))/2^16;

%%Colour Balancing
rgb2xyz = [0.5767309,0.1855540,0.1881852; 0.2973769,0.6273491,0.0752741; 0.0270343, 0.0706872, 0.9911085]; 
xyz2cam = [6461,-907,-882;-4300,12184,2378;-819,1944,5931]./10000;
rgb2cam = rgb2xyz * xyz2cam; 
rgb2cam = rgb2cam./repmat(sum(rgb2cam,2),1,3);
cam2rgb = rgb2cam^-1;
lin_srgb = apply_cmatrix(lin_rgb,cam2rgb);
lin_srgb = max(0,min(lin_srgb,1));

final_image = lin_srgb;

end