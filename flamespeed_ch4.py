
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
phi = 0.9

width = 0.03  # m

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('gri30.xml', 'gri30_mix')
gas.TP = Tin, p
gas.set_equivalence_ratio(phi, 'CH4', 'O2:1.0, N2:3.76')

# Flame object
f = ct.FreeFlame(gas, width=width)
f.set_refine_criteria(ratio=3, slope=0.07, curve=0.14)

f.solve(loglevel=1, auto=True)
print('\nmixture-averaged flamespeed = {:7f} m/s\n'.format(f.u[0]))

plt.figure('Fig.1')
plt.subplot(2,1,1)
plt.plot(f.grid, f.T)
plt.xlabel('Axial distance [m]')
plt.ylabel('Temperature [K]')
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(f.grid, f.u)
plt.xlabel('Axial distance [m]')
plt.ylabel('Flame speed [m/s]')
plt.tight_layout()
plt.grid(True)
plt.show()