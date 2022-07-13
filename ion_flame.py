
import cantera as ct

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
phi = 1.0
width =  0.03 # [m]

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('gri30_ion.yaml')
gas.TP = Tin, p
gas.set_equivalence_ratio(phi, 'CH4', 'O2:1.0, N2:3.76')

# Flame object
f = ct.IonFreeFlame(gas, width=width)
f.set_refine_criteria(ratio=3, slope=0.07, curve=0.14)

f.solve(loglevel=1, auto=True)
f.solve(loglevel=1, stage=2, enable_energy=True)

f.write_csv('ion_flame.csv', quiet=False)
