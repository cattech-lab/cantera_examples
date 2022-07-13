"""
Constant-pressure, adiabatic kinetics simulation with sensitivity analysis
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import cantera as ct

# conditions
gas = ct.Solution('gri30.yaml')
temp = 1500.0
pres = ct.one_atm
phi = 1.0

gas.TP = temp, pres
gas.set_equivalence_ratio(phi, 'CH4', 'O2:1.0, N2:3.76')
r = ct.IdealGasConstPressureReactor(gas, name='R')
sim = ct.ReactorNet([r])

# all reactions with respect to the temperature sensitivity
nreac = 325
for i in range(nreac):
    r.add_sensitivity_reaction(i)

# set the tolerances for the solution and for the sensitivity coefficients
sim.rtol = 1.0e-6
sim.atol = 1.0e-15
sim.rtol_sensitivity = 1.0e-6
sim.atol_sensitivity = 1.0e-6

# time loop
smax = [0]*nreac
for t in np.arange(0, 2e-3, 5e-6):
    sim.advance(t)

    # sensitivities for each reaction
    for i in range(nreac):
        s = sim.sensitivity('temperature', i) # sensitivity of temperature to reaction
        if abs(s) > abs(smax[i]): # maximum sensitivity
            smax[i] = s

    print('time: {:12.7f}'.format(t))        

print('\n---------------- Sensitivity for all reactions --------------- \n') 
for i in range(nreac):
    print('{:3d} {:<35s} {:14.6f}'.format(i + 1, sim.sensitivity_parameter_name(i), smax[i])) 

# top 10
ntop = 10
smax_sort = sorted(smax, key=abs, reverse=True) 
smax_indx = [smax.index(x) for x in smax_sort]

rlabel = []
sp = []

print('\n---------------- Sensitivity for Top 10 reactions --------------- \n') 
for i in range(ntop):
    rlabel.append(sim.sensitivity_parameter_name(smax_indx[i]))
    sp.append(smax_sort[i])
    print('{:3d} {:5d} {:<35s} {:14.6f}'.format(i, smax_indx[i] + 1, rlabel[i], sp[i]))   

# plot
plt.title('Sensitivity for Temperature')
plt.barh(rlabel, sp)
plt.xlabel('Sensitivity')
plt.gca().invert_yaxis()
plt.gca().set_axisbelow(True)
plt.grid(axis='x')
plt.tight_layout()
plt.show()