%%Writen by Christopher Duffy

function [ Magnitude ] = Magnitude(Photon_Count)
%%Function takes an input photon count and converts it to a magnitude for
%%the central frequency of the sun, as used in the DarkSky function.

%%Wavelength
Wavelength = 517*10^-9;

%%Required Constants
h = 6.626*10^-34;
A = pi*(40*10^-3)^2; 
Flux_Vega = 2.176*10^-6;
c = 2.998*10^8;
Transmission_Coefficient = 0.9;

%%Magnitude
Magnitude = -2.5*log10(((Photon_Count*(h*(c/Wavelength))/Transmission_Coefficient)/A)/Flux_Vega);

end