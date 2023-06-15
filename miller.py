from numpy import *

A=2.2
kappa=1.5
delta=0.3
R0=2.5
theta=linspace(0,2*pi)
r=R0/A
R_s=R0+r*cos(theta+(arcsin(delta)*sin(theta)))
Z_s=kappa*r*sin(theta)

import matplotlib.pyplot as plt

plt.plot(R_s, Z_s)
plt.axis("equal")
plt.xlabel("R [m]")
plt.ylabel("Z [m]")
plt.savefig("/home/peter/Documents/RDM_RSE_Masterclass_20230712/automate_script/miller.png")
