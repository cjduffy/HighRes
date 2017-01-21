function [ Corrected_Image ] = darkflat(Raw, Image_Name)
%%Written by Michael Wright

%%Darkflat function takes an image and the image metadata, and uses this to
%%find the correct Flat Field, Flat Field Dark Current, and Dark Current to
%%correct the input image with, and performs this correction.

%%Create Exposure Time Variable
Information = imfinfo(Image_Name);
Exposure_Time = Information.DigitalCamera.ExposureTime;

%%Go to Flat Field Folder
cd('/home/mick/EclipseData/Flat Fields')
%%Read in Correct Flat Field
Flat_Folder_Contents = dir('*.tiff');

for i=1:length(Flat_Folder_Contents)
    Flat_Untrimmed_Name = Flat_Folder_Contents(i).name;
    Flat_Name = strtrim(Flat_Untrimmed_Name);
    Flat_MetaData = imfinfo(Flat_Name);
    Flat_Exposure = Flat_MetaData.DigitalCamera.ExposureTime;
 
    if Flat_Exposure == Exposure_Time
        Flat_Field = double(imread(Flat_Name));
       cd('/home/mick/Downloads')
        Flat_Field = ProcessParTwo(ProcessParOne(Flat_Field));
         cd('/home/mick/EclipseData/Flat Fields')
        break
    else 
        Flat_Field = 'null';
    end
    
end 

%%Go to Dark Flat Field Folder
cd('/home/mick/EclipseData/Flat Field - Dark Current')
Dark_Flat_Folder_Contents = dir('*.tiff');

for j=1:length(Dark_Flat_Folder_Contents)
    Dark_Flat_Untrimmed_Name = Dark_Flat_Folder_Contents(j).name;
    Dark_Flat_Name = strtrim(Dark_Flat_Untrimmed_Name);
    Dark_Flat_MetaData = imfinfo(Dark_Flat_Name);
    Dark_Flat_Exposure = Dark_Flat_MetaData.DigitalCamera.ExposureTime;
    
   
      if Dark_Flat_Exposure == Exposure_Time
        Dark_Flat_Field = double(imread(Dark_Flat_Name));
        cd('/home/mick/Downloads')
        Dark_Flat_Field = ProcessParTwo(ProcessParOne(Dark_Flat_Field));
         cd('/home/mick/EclipseData/Flat Field - Dark Current')
        break
    else
        Dark_Flat_Field = 'null';
      end
end

%%Go to Dark Current Folder
cd('/home/mick/EclipseData/Dark Current')
Dark_Folder_Contents = dir('*.tiff');

for k=1:length(Dark_Folder_Contents)
    Dark_Untrimmed_Name = Dark_Folder_Contents(k).name;
    Dark_Name = strtrim(Dark_Untrimmed_Name);
    Dark_MetaData = imfinfo(Dark_Name);
    Dark_Exposure_Time = Dark_MetaData.DigitalCamera.ExposureTime;
    
    
    if Dark_Exposure_Time == Exposure_Time 
      Dark_Current = double(imread(Dark_Name));
      if size(Dark_Current,1) ~= 3465
          Dark_Current_To_Remove = transpose(Dark_Current);
           cd('/home/mick/Downloads')
          Dark_Current_To_Remove = ProcessParTwo(ProcessParOne(Dark_Current_To_Remove));
          cd('/home/mick/EclipseData/Dark Current')
      else
          cd('/home/mick/Downloads')
          Dark_Current_To_Remove = ProcessParTwo(ProcessParOne(Dark_Current));
          cd('/home/mick/EclipseData/Dark Current')
      end 
      break
    else 
        Dark_Current_To_Remove = 'null';
    end
end

%%Perform Correction
Flat_Dark_Corrected = Flat_Field - Dark_Flat_Field;
Av_Flat_Dark = mean(Flat_Dark_Corrected(:));
Gain = Av_Flat_Dark./Flat_Dark_Corrected;
Image_Dark_Corrected = Raw - Dark_Current_To_Remove;
Corrected_Image = Image_Dark_Corrected.*Gain;

cd('/home/mick/Downloads')

end 