function [ Photon_Count ] = PhotonCount(Magnitude)
%%By Michael Wright

%%Function takes an input magnitude and converts it to a photon count for
%%the average central frequencies of red, blue, and green, as used in the
%%Glare Removal function.

%%Required Constants
h = 6.626*10^-34;
A = pi*(40*10^-3)^2; 
Flux_Vega = 2.176*10^-6;
c = 2.998*10^8;
Transmission_Coefficient = 0.9;
Wavelength = (2.9*10^-3)/5772;

%%Photon Count
Photon_Count = (A*10^(-0.4*Magnitude)*Flux_Vega*Transmission_Coefficient)/(h*(c/Wavelength));

end