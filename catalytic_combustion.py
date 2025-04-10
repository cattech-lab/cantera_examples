"""
Catalytic combustion of methane on platinum.
"""

import numpy as np
import cantera as ct

#  parameter
p = ct.one_atm  # pressure [Pa]
tinlet = 300.0  # inlet temperature [K]
tsurf = 900.0  # surface temperature [K]
mdot = 0.06  # inlet flux [kg/m^2/s]
width = 0.1 # inlet/surface separation [m]
comp = 'CH4:0.095, O2:0.21, N2:0.78, AR:0.01' # inlet composition

# gas object
gas = ct.Solution('ptcombust.yaml', 'gas')
gas.TPX = tinlet, p, comp

# interface object
surf_phase = ct.Interface('ptcombust.yaml', 'Pt_surf', [gas])
surf_phase.TP = tsurf, p

# integrate the coverage equations in time for 1 s, for initial 
surf_phase.advance_coverages(1.0)

# impinging jet object
sim = ct.ImpingingJet(gas=gas, width=width, surface=surf_phase)
sim.inlet.mdot = mdot
sim.inlet.T = tinlet
sim.inlet.X = comp
sim.surface.T = tsurf

# solve
sim.set_refine_criteria(3.0, 0.06, 0.12, 0.0)
sim.solve(loglevel=1, auto=True)
sim.show()

# write csv file 
sim.save('catalytic_combustion.csv', basis='mole', overwrite=True)
