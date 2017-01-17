function [ Photon_Count ] = PhotonCount(Magnitude)
%%Function takes an input magnitude and converts it to a photon count for
%%the average central frequencies of red, blue, and green, as used in the
%%Glare Removal function.

%%RGB Wavelengths
R_Wavelength = 680*10^-9;
G_Wavelength = 532.5*10^-9;
B_Wavelength = 472.5*10^-9;

%%Required Constants
h = 6.626*10^-34;
A = pi*(40*10^-3)^2; 
Flux_Vega = 2.176*10^-6;
c = 2.998*10^8;
Transmission_Coefficient = 0.9;

%%Photon Count
R_Photon_Count = (A*10^(-0.4*Magnitude)*Flux_Vega*Transmission_Coefficient)/(h*(c/R_Wavelength));
G_Photon_Count = (A*10^(-0.4*Magnitude)*Flux_Vega*Transmission_Coefficient)/(h*(c/G_Wavelength));
B_Photon_Count = (A*10^(-0.4*Magnitude)*Flux_Vega*Transmission_Coefficient)/(h*(c/B_Wavelength));

%%Output Vector
R_Real_Photon_Count = PlanckWeight(R_Wavelength)*R_Photon_Count;
G_Real_Photon_Count = PlanckWeight(G_Wavelength)*G_Photon_Count;
B_Real_Photon_Count = PlanckWeight(B_Wavelength)*B_Photon_Count;

Photon_Count = G_Real_Photon_Count + B_Real_Photon_Count + R_Real_Photon_Count;

end