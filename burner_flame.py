"""
Burner-stabilized flat flame of the premixed hydrogen-oxygen 
"""

import cantera as ct

# Simulation parameters
p = 0.05 * ct.one_atm # pressure [Pa]
Tin = 373.0 # temperature [K]
mdot = 0.06 # mass flux [kg/s/m^2]
comp = 'H2:1.5, O2:1, AR:7'  # premixed gas composition
width = 0.5  # region width [m]

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('h2o2.yaml')
gas.TPX = Tin, p, comp

# Set up flame object
f = ct.BurnerFlame(gas, width=width)
f.burner.mdot = mdot
f.set_refine_criteria(ratio=3.0, slope=0.05, curve=0.1)
f.show_solution()

# Solve
f.transport_model = 'Multi'
f.solve(loglevel=1, auto=True)
f.show_solution()

# write the velocity, temperature, density, and mole fractions to a CSV file
f.write_csv('burner_flame.csv', quiet=False)