High Resolution Imaging:
The aim of the project is to write software to analyse input images and 
process them with a view to creating aesthetically pleasing images that 
have as few astronomical errors as possible

Possible Observation Targets:
The Moon - Individual Craters?
Andromeda
Triangulum
Rings of Saturn/Moons of Saturn
Crab Nebula
Non-Galilean Moons of Jupiter
Centauri System
M110
Mars
Possible Others - add to the readme at your leisure

Goals for 24/01/17

Investigate equipment - capabilities and limitations
Investigate software - tracking capabilities and customisability
Establish the degree of automation that is feasible
Begin process of converting code from MATLAB to C as a test of 
feasibility for writing all software for the project in C

Equipment

Meade Telescope
QHY5-II

Means the theorhetical resolution of the system is
R = wavelength/D = 0.28"
Telescope is seeing limited (seeing = 2") so the goal would be to push 
the accuracy above the seeing limit. 
Each pixel has an area of capture of 0.284"*0.281" = 0.080(arc^2)

Software Concerns
Can use MATLAB to create sample data for the software to unblur as a 
testing scenario before moving on to actual data
Registration - use RegiStar as a benchmarking program

User should have a choice between:
Statistical approaches to image corrections
Other image based corrections

Layering multiple wavelength images together (and Image Stitching)
Fast Fourier Transformation
Wavelet Filtering
Distortions
Median Filtering
