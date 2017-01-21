a=30; %lunar phase angle
Z=71; %Zenith of sky
z=60; %Zenith distance of moon
k=0.172; %extinction coefficeint 
b=79; %background brightness 

for p=1:0.01:5 %moon sky seperation this is the thing we need to integrate over

I=10^(-0.4*(3.84+(0.026*abs(a))+4*10^-9*a^4));

f=(10^5.36)*(1.06+cos(p)^2)+10^(6.15-p/40);

X=(1-0.96*sin(Z)^2)^-0.5;

x=(1-0.96*sin(z)^2)^-0.5;

B=f*I*10^(-0.4*k*x)*(1-10^(-0.4*k*X))

deltaV=-2.5*log10((B-b)/b)

end