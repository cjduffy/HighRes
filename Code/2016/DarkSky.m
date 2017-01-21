%%Written by Christopher Duffy

%%This script takes images and dark currents and performs a subtraction
%%from each image of the dark current of corresponding exposure length. It
%%then finds the mean digital number count for each image and from that
%%caluclates the brightness in nanoLamberts.

%%Required constants
number_images = length(dir('*.tif'));
starting_number = 4076;
gain = 1.405;
QE = 0.4;
A = cell(1,length(dir('*tif')));
B = zeros(2,number_images);


for i = (starting_number : starting_number + number_images - 1);
    %%Set exposure time variable 
Name = strtrim(sprintf('IMG_%d.tif', i));
Information = imfinfo(Name);
Exposure_Time = Information.DigitalCamera.ExposureTime;

%%Go to dark currents    
cd('/Users/chrisduffy/Documents/MATLAB/Solar Eclplise/7th March Dark Sky and Dark Current/Dark Currents')
Dark_Folder_Contents = dir('*.tif');

for k=1:length(Dark_Folder_Contents)
    Dark_Untrimmed_Name = Dark_Folder_Contents(k).name;
    Dark_Name = strtrim(Dark_Untrimmed_Name);
    Dark_MetaData = imfinfo(Dark_Name);
    Dark_Exposure_Time = Dark_MetaData.DigitalCamera.ExposureTime;
    
      if Dark_Exposure_Time == Exposure_Time
        Dark_Current = double(imread(Dark_Name));
        break
     else 
        Dark_Current = 'null';
     end
    
end
%%Go to images
cd('/Users/chrisduffy/Documents/MATLAB/Solar Eclplise/7th March Dark Sky and Dark Current/Light Polluted')

for j = (starting_number : starting_number + number_images - 1);
    Name2 = strtrim(sprintf('IMG_%d.tif', j));
    Information2 = imfinfo(Name2);
    Image = double(imread(sprintf('IMG_%d.tif',j)));
    Image_Exposure_Time = Information2.DigitalCamera.ExposureTime;
   
    if Image_Exposure_Time == Exposure_Time
    Corrected = Image - Dark_Current;
   
    else
        Corrected = 'null';
        break
    end
    
    mean_image=mean(Corrected(:));
    
    A{1,j} = mean_image;
    
   Digital_Number_Per_Pixel = mean_image;
   Photon_Count_Per_Pixel = (Digital_Number_Per_Pixel/QE)*gain;
   Mag_per_pixel = Magnitude(Photon_Count_Per_Pixel);
   Mag_per_arc = (Mag_per_pixel/3.17); 
   Average_Brightness = 10^(-0.4*(Mag_per_arc-26.33));
    %%Generate output array of average brightnesses at corresponding
    %%exposure times.
B(1,j-4075) = Average_Brightness
B(2,j-4075) = Information.DigitalCamera.ExposureTime    
end

end