%%Writen by Christopher Duffy

%%This script performs the Astrometric_Analyis Function and writes the
%%Output as a .tiff file with the name format "Final_Image_X.tiff" where X
%%is the number in in the for loop

number_images = length(dir('*.tiff'));
Folder_Contents = dir('*.tiff');

for i = 1:number_images
    
    image = Folder_Contents(i).name;
    
    Final_Image = Astrometric_Analysis(image);

    imwrite(Final_Image, sprintf('Final_Image_%d.tiff',i));
    
end