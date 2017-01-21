function [ Images_Glare_Removed ] = GlareRem(Image, Information, End)

%%Function removes the Lunar Glare from images in an effort to counteract
%%the effect on the position of the luminosity spike of stars in the image.
%%I.e the moon's glare moves the centroid of the spike towards the moon.
 
%%Quantities needed for function - camera pixel field size, furthest
%%possible distance, Lunar Phase Angle, and the Lunar Intensity as defined
%%by the 'Model of the Brightness of Moonlight' Paper.
Quantum_Efficiency = 0.4;
Gain = 1.405;
Res= (1.78)/3600;
Phase_Angle = 0; 
Intensity = 10^(-0.4*(3.84 + 0.26*abs(Phase_Angle) + (4*10^9)*Phase_Angle^4));
Glare_Digital_Number_Per_Pixel = zeros(1,length(End/Res));
Image_Glare_Removed = zeros(3465,5202);

%%For loop, calculates the magnitude of the glare for a pixel up to the
%%maximum possible pixel distance for the image. 
for Theta=Res:Res:End
    n = int16(Theta/Res)
    %%Glare as defined by the paper
    Glare = (4.7*10^7 + (4.4*10^5/(Res*3.14)))*Intensity*(Theta^-2);
    %%Conversion from nano-Lamberts to mag per square arc
    Glare_Mag_Per_Square_Arc = 26.33 - 2.5*(log10(Glare));
    %%Conversion from per square arc to per pixel
    Glare_Mag_Per_Pixel = Glare_Mag_Per_Square_Arc*3.17;
    %%Conversion to Glare Photon Count Per Pixel
    Glare_Photon_Count_Per_Pixel = PhotonCount(Glare_Mag_Per_Pixel);
    %%Conversion to Digital Number
    Glare_Digital_Number_Per_Pixel_Per_Second = (Quantum_Efficiency*Glare_Photon_Count_Per_Pixel)/Gain;
    %%Conversion to Digital Number for Time
    Glare_Digital_Number_Per_Pixel(1,n) = Glare_Digital_Number_Per_Pixel_Per_Second*1; %replace the command for structures here
end

%%Call the centroid function
Ce = centroid(Image);

parfor i = 1:3465
    for j = 1:5202
        i
        %%Formula for X-distance from Centroid
        x_distance = int16(abs(Ce(1,1)-i));
        %%Formula for Y-distance from Centroid
        y_distance = int16(abs(Ce(1,2)-j));
        
        %%Value of Glare at x distance
        if x_distance ~= 0 
            x_glare = Glare_Digital_Number_Per_Pixel(1,x_distance);
        else
            x_glare = 0;
        end
        %%Value of Glare at y distance
        if y_distance ~= 0
            y_glare = Glare_Digital_Number_Per_Pixel(1,y_distance);
        else
            y_glare = 0;
        end
        %%Value of Glare to Remove
        
        %%Exclusion for the area that the moon takes up, this may need it's
        %%value altered to be more accurate. It doesn't use sqrt because
        %%parfor takes an issue with it for some reason which is why the
        %%500 is squared instead.
        if x_distance^2+y_distance^2 <= 500^2 
        Glare_to_Remove = 0;
        
        else
        
        Glare_to_Remove = sqrt(x_glare^2+y_glare^2);
        end 
        %%Correct Image
        Images_Glare_Removed(i,j) = Image(i,j) - Glare_to_Remove;
    end 
end
end
    