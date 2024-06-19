"""
Counter flow diffusion flame
"""

import cantera as ct

# Simulation parameters
p = ct.one_atm  # pressure [Pa]

Tin_fuel = 300.0  # fuel inlet temperature [K]
mdot_fuel = 0.2  # fuel mass flux [kg/s/m^2]
comp_fuel = "CH4:1"  # fuel composition

Tin_oxi = 300.0  # oxidizer inlet temperature [k]
mdot_oxi = 0.8  # oxidizer mass flux [kg/s/m^2]
comp_oxi = "O2:0.21, N2:0.78, AR:0.01"  # oxidizer composition

width = 0.02  # Distance between inlets [m]

# Gas object
gas = ct.Solution("gri30.yaml")
gas.TP = Tin_oxi, p

# Flame object
f = ct.CounterflowDiffusionFlame(gas, width=width)

f.fuel_inlet.mdot = mdot_fuel
f.fuel_inlet.X = comp_fuel
f.fuel_inlet.T = Tin_fuel

f.oxidizer_inlet.mdot = mdot_oxi
f.oxidizer_inlet.X = comp_oxi
f.oxidizer_inlet.T = Tin_oxi

f.set_refine_criteria(ratio=3.0, slope=0.05, curve=0.1, prune=0.05)

# Solve
f.solve(loglevel=1, auto=True)
f.show()

# write the velocity, temperature, and mole fractions to a CSV file
f.save("counter_diffusion_flame.csv", basis="mole", overwrite=True)
