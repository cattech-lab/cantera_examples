
import cantera as ct
import csv

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 1500.0  # inlet temperature [K]
comp = 'CH4:1, O2:1, AR:0.5' 
vin = 0.005 # inlet velocity [m/s]
length = 5e-6 # reactor length [m]
area = 1e-4 # cross section area [m2]
n_reactor = 200 # number of divided reactor

# define object
gas = ct.Solution('gri30.yaml')
gas.TPX = Tin, p, comp
mdot = vin * area * gas.density
dx = length / n_reactor

r = ct.IdealGasReactor(gas)
r.volume = area * dx

upstream = ct.Reservoir(gas, name='upstream')
downstream = ct.Reservoir(gas, name='downstream')
m = ct.MassFlowController(upstream, r, mdot=mdot)
v = ct.PressureController(r, downstream, master=m, K=1.0e-5)

sim = ct.ReactorNet([r])

# solve
outfile = open('pfr.csv','w', newline='')
writer = csv.writer(outfile)
writer.writerow(['Distance (m)', 'u(m/s)', 'rtime(s)', 'T(K)', 'P(Pa)'] + gas.species_names)

t_res = 0.0
for n in range(n_reactor):
    gas.TDY = r.thermo.TDY
    upstream.syncState()
    sim.reinitialize()
    sim.advance_to_steady_state()
    dist = n * dx
    u = mdot / area / r.thermo.density # velocity
    t_res += r.mass / mdot  # residence time 
    writer.writerow([dist, u, t_res, r.T, r.thermo.P] + list(gas.X))

outfile.close()
