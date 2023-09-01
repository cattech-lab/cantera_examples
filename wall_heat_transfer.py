
import cantera as ct
import csv
import math

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 20.0 + 273.15  # inlet temperature [K]
comp = 'O2:1.0, N2:3.76' 
vin = 1.0 # inlet velocity [m/s]
length = 2.0 # reactor length [m]
area = math.pi * 0.1 * 0.1 / 4.0 # cross section area [m2]
n_reactor = 200 # number of divided reactor

Tout = 100.0 + 273.15 # outer temperature [K] 
area_wall = math.pi * 0.1 * length # heat transfer wall area [m2]
ht = 50.0 # heat transfer coef. [W/m2/K]

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
v = ct.PressureController(r, downstream, primary=m, K=1.0e-5)

gas.TPX = Tout, p, comp
outer = ct.Reservoir(gas)
wall = ct.Wall(outer, r, U=ht)
wall.area = area_wall / n_reactor  

sim = ct.ReactorNet([r])

# solve
outfile = open('wall_heat_transfer.csv','w', newline='')
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
    writer.writerow([dist, u, t_res, r.T, r.thermo.P] + list(r.thermo.X))

outfile.close()
