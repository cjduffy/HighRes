#!/usr/bin/env python2
import numpy

def GlareRem (Image, Information, End):
	"This function does stuff"
	Quantum_Efficiency = 0.4;
	Gain = 1.405;
	Res= (1.78)/3600;
	Phase_Angle = 0; 
	Intensity = 10**(-0.4*(3.84 + 0.26*abs(Phase_Angle) + (4*10**9)*Phase_Angle**4));
	Glare_Digital_Number_Per_Pixel = np.zeros((End/Res));
	Image_Glare_Removed = zeros(3465,5202);

	for Theta in list(range(Res,End, Res)):
		n = int(Theta/Res)
    ##Glare as defined by the paper
	Glare = (4.7*10^7 + (4.4*10**5/(Res*3.14)))*Intensity*(Theta**-2);
    ##Conversion from nano-Lamberts to mag per square arc
	Glare_Mag_Per_Square_Arc = 26.33 - 2.5*(log10(Glare));
    ##Conversion from per square arc to per pixel
	Glare_Mag_Per_Pixel = Glare_Mag_Per_Square_Arc*3.17;
    ##Conversion to Glare Photon Count Per Pixel
	Glare_Photon_Count_Per_Pixel = PhotonCount(Glare_Mag_Per_Pixel); ##FUNCTION CALL, ADD PATH
    ##Conversion to Digital Number
	Glare_Digital_Number_Per_Pixel_Per_Second = (Quantum_Efficiency*Glare_Photon_Count_Per_Pixel)/Gain;
    ##Conversion to Digital Number for Time
	Glare_Digital_Number_Per_Pixel[1,n] = Glare_Digital_Number_Per_Pixel_Per_Second*1; 
		

	return[Image_Glare_Removed]
