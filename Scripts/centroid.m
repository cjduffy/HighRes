function [ centroid ] = centroid(Image)
%%function takes an image and determines the centroid of the Moon, it does
%%this by converting the image from digital number to magnitude, and then,
%%picking a point in the glare, using that to create an arc of the same
%%magnitude and using the circle fit function to establish the centre of
%%the complete circle of that arc. 
Quantum_Efficiency = 0.40;
Gain = 1.405;
Image_Photon_Count = zeros(5202,3465);
%%For loop converts the image from digital number to magnitude
for i = 1:3465
    for j = 1:5202
        %%Convert to Photon Count
        Image_Photon_Count(i,j) = (Image(i,j)*Gain)/Quantum_Efficiency;
    end
end

Point_of_Consideration = Image_Photon_Count(2562,1304);
[x,y] = find(Image>Point_of_Consideration-50 & Point_of_Consideration+50);

[xc,yc,R] = circfit(x,y);
centroid = [int16(xc),int16(yc)];

end