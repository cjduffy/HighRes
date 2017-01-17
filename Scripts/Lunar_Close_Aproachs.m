clc
t1 = datetime(2016,01,25,0,0,0);
t2 = datetime(2016,03,24,0,0,0);
t = t1:minutes(1):t2;
h = pi/12;
m = pi/720;
s = pi/43200;
RA_Reg = (10*h+08*m+22.311*s); 
Dec_Reg = (dms2degrees(11, 58, 01.95)*(pi/180));
RA_moon = (Hour.*h+Minute.*m+Seconds.*s);
Dec_moon = (dms2degrees(Degrees, Min_dec, Sec_dec)*(pi/180));
RA_jup = (hourjup.*h+minutejup.*m+secondjup.*s);
Dec_jup = (dms2degrees(degreejup, minutedecjup, seconddecjup)*(pi/180));
RA=RA_Reg-RA_moon;
Dec=Dec_Reg-Dec_moon;
%distance= sqrt(RA.^2+Dec.^2);
x=sin(Dec_jup).*sin(Dec_moon)+cos(Dec_jup).*cos(Dec_jup).*cos(RA_jup-RA_moon);
distance=  acos(x).*(180/pi);
plot(t,distance, 'x')