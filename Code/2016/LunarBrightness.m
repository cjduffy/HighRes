function [ Corrected_Image ] = LunarBrightness(Image, Information)
%%By Michael Wright 

%%Function creates a model of the brightenss of the sky caused by the Moon
%%and then corrects the image fed in to it. This is done using the model
%%created by the paper 'A Model on the Brightness of Moonlight'

%%Constants needed for the function
Phase = (1-0.984)*180;
Zenith_Moon = 52.62;
Background = 79;
Zenith_Sky = 90-55.9;
Extinction = 0.2; 
Quantum_Efficiency = 0.4;
Gain = 1.405;
Res= (1.78)/3600;
Digital_Number_Per_Pixel = zeros(1,length(5/Res));
Corrected_Image = zeros(3465,5202);


%%For loop runs the surface brightness model for a particular distance to
%%the moon, then converts that to the correct Digital Number for that pixel
%%distance. This is run over moon-sky distances at the resolution of the
%%camera. 
for theta=Res:Res:5
    %%Calculate N
    n = int16(theta/Res);
    %%Calculate the Intensity
    Intensity=10^(-0.4*(3.84+(0.026*abs(Phase))+4*10^-9*Phase^4));
    %%Calculate the Scattering Function
    Scatter=(10^5.36)*(1.06+cos(theta)^2)+10^(6.15-theta/40);
    %%Calculate the Optical Path Length to Sky
    Path_Sky=(1-0.96*sin(Zenith_Sky)^2)^-0.5;
    %%Calculate the Optical Path Length to Moon
    Path_Moon = (1-0.96*sin(Zenith_Moon)^2)^-0.5;
    %%Calculate the Surface Brightness of the Moon
    Surface_Brightness=Scatter*Intensity*10^(-0.4*Extinction*Path_Moon)*(1-10^(-0.4*Extinction*Path_Sky));
    %%Calculate thus the change in magnitudes
    Change_Magnitude_Per_Res = -2.5*log10((Surface_Brightness-Background)/Background);
    %%Calculate Magnitude
    Prop_Mag = Change_Magnitude_Per_Res + 21.587;
    %%Calculate the change in Photon Count
    Photon_Count_Per_Res = PhotonCount(Prop_Mag);
    %%Calculate the Digital Number Per Second
    Digital_Number_Per_Second = (Quantum_Efficiency*Photon_Count_Per_Res)/Gain;
    %%Calculate the Digital Number Per Pixel
    Digital_Number_Per_Pixel(1,n) = Digital_Number_Per_Second*Information.DigitalCamera.ExposureTime;
end 

%%Call the Centroid Function
Ce = centroid(Image);

parfor i = 1:3465
    for j = 1:5202
        %%Formula for X-distance from Centroid
        x_distance = int16(abs(Ce(1,1)-i));
        %%Formula for Y-distance from Centroid
        y_distance = int16(abs(Ce(1,2)-j));
        
        %%Value of brightness at x distance - the value of the brightness Digital
        %%Number at the x-distance, assuming not at centre. If at centre,
        %%set glare to zero.
        if x_distance ~= 0 
            x_glare = Digital_Number_Per_Pixel(1,x_distance);
        else
            x_glare = 0;
        end
        
        %%Value of brightness at y distance - the same rules apply as for the
        %%x-distance
        if y_distance ~= 0
            y_glare = Digital_Number_Per_Pixel(1,y_distance);
        else
            y_glare = 0;
        end
        
        %%Value of Digital Number to Remove - with an exclusion for being inside of
        %%the moon. The moon's pixel distance is determined to be five
        %%hundred pixels. The justification for this being that in the
        %%image in which the moon is completely within shot, the radius of
        %%the moon is five hundred pixels. 
        if x_distance^2+y_distance^2 <= 500^2 
        DN_to_Remove = 0;
        else
        DN_to_Remove = sqrt(x_glare^2+y_glare^2);
        end
        
        %%Correct Image
        Corrected_Image(i,j) = Image(i,j) - DN_to_Remove;
    end 
end

