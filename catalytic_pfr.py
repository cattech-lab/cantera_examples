
import cantera as ct
import csv

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 918.15  # inlet temperature [K]
comp = 'CH4:0.14, O2:1, N2:3.76' 
vin = 16.7 # inlet velocity [m/s]
length = 0.2 # reactor length [m]
area = 1.267e-6 # cross section area [m2]
n_reactor = 200 # number of divided reactor
area_cat_vol = 3149.0 # catalyst area [m2/m3]
porosity = 1.0 # catalyst porosity

# define object gas
file_name = 'ptcombust.yaml'
gas = ct.Solution(file_name, 'gas')
gas.TPX = Tin, p, comp
mdot = vin * area * gas.density
dx = length / n_reactor

# define object surface
surf = ct.Interface(file_name, 'Pt_surf', [gas])
surf.TP = Tin, p

# define object reactor
r = ct.IdealGasReactor(gas)
vol = area * dx * porosity
r.volume = vol

upstream = ct.Reservoir(gas, name='upstream')
downstream = ct.Reservoir(gas, name='downstream')
m = ct.MassFlowController(upstream, r, mdot=mdot)
v = ct.PressureController(r, downstream, primary=m, K=1.0e-5)

area_cat = area_cat_vol * vol
rsurf = ct.ReactorSurface(surf, r, A=area_cat)

sim = ct.ReactorNet([r])

# solve
outfile = open('catalytic_pfr.csv','w', newline='')
writer = csv.writer(outfile)
writer.writerow(['Distance (m)', 'u(m/s)', 'rtime(s)', 'T(K)', 'P(Pa)'] + gas.species_names + surf.species_names)

t_res = 0.0
for n in range(n_reactor):
    gas.TDY = r.thermo.TDY
    upstream.syncState()
    sim.reinitialize()
    sim.advance_to_steady_state()
    dist = n * dx
    u = mdot / area / r.thermo.density # velocity
    t_res += r.mass / mdot  # residence time 
    writer.writerow([dist, u, t_res, r.T, r.thermo.P] + list(gas.X) + list(surf.coverages))

outfile.close()
