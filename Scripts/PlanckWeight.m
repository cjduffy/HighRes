function [ Weighting ] = PlanckWeight(Wavelength)
%%function creates the amount of weighting required for a particular
%%wavelength's intensity in the image based on the Planck Formula. 

%%Constants used in Planck Law
%%Planck Constant
h = 6.626*10^-34;
%%Speed of Light
c = 2.998*10^8;
%%Boltzmann Constant
k = 1.381*10^-23;
%%Solar Photospheric Temperature
T = 5778;
%%Solar Maximum Frequency
Wavelength_Max = (2.9*10^-3)/T;

%%Calculate value of Planck Law for interested Wavelength
B_v = ((2*h*c^2)/(Wavelength)^5)*1/(exp((h*c)/(Wavelength*k*T))-1);
%%Calculate maximal Planck Law 
B_max = ((2*h*c^2)/(Wavelength_Max)^5)*1/(exp((h*c)/(Wavelength_Max*k*T))-1);
%%Calculate Weight
Weighting = B_v/B_max;

end 