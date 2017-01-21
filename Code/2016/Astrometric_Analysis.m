function [ Final_Image ] = Astrometric_Analysis(Image)
%%Written by Michael Wright

%%This function performs all the analytical functions for the 'Analysing
%%Solar Eclipse Data' lab, as constructed by the lab authors. It does this
%%by taking in the name of an image and then using that data to create the
%%results for the rest of the functions. 
Raw_Image = double(imread(Image));

%%Stage One: Perform the correction functions for the Lunar Glare caused
%%by the optics in the image, and the effect of the Lunar Surface
%%Brightness on the Brightness of the Night Sky. These functions require
%%the metadata of the image. 
MetaData = imfinfo(Image);
Glare_Removed_Image = GlareRem(Raw_Image, MetaData);
Lunar_Corrected_Image = LunarBrightness(Glare_Removed_Image, MetaData);

%%Stage Two: Read in the tiff image and perform the initial image stages
%%of linearisation and white balancing, which then allows the rest of the
%%data manipulation to occur.
Initial_Process_Image = ProcessParOne(Lunar_Corrected_Image);

%%Stage Three: Perform the final half of the raw image processing by
%%demosaicing and performing the colour balancing and colour space
%%conversion - this should result in a similar kind of image as to those
%%processed completely, but with the corrections that are done. 
Second_Process_Image = ProcessParTwo(Initial_Process_Image);

%%Stage Four: Perform the dark current and flat field removal. The
%%justification for doing this now is that the dark current and flat fields
%%have to themselves be processed in order to correct the image properly -
%%since the dark current is not in and of itself homogenous amongst the
%%three colours. 
Final_Image = darkflat2(Second_Process_Image, Image);
end




