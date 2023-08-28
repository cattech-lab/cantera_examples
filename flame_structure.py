"""
A freely-propagating, premixed hydrogen flat flame with multicomponent
transport properties.
"""

import cantera as ct
import numpy as np

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
phi = 1.0 # equivalence ratio
width = 2.0 # region width [m]

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('sandiego20161214_H2only.yaml')
gas.TP = Tin, p
gas.set_equivalence_ratio(phi, 'H2', 'O2:1.0, N2:3.76')

# Set up flame object
f = ct.FreeFlame(gas, width=width)
f.set_refine_criteria(ratio=3, slope=0.06, curve=0.12)

# Solve 
f.transport_model = 'multicomponent'
f.solve(loglevel=1, auto=True)
f.show_solution()

# write the velocity, temperature, density, and mole fractions to a CSV file
f.save('h2_flame.csv', basis='mole', overwrite=True)
