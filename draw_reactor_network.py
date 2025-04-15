
import cantera as ct

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 1000.0  # inlet temperature [K]
comp_in = 'CH4:0.5, O2:1.0, N2:3.76'  # inlet component

Toutside = 300.0  # outside temperature [K] 
comp_outside = 'O2:1.0, N2:3.76'  # outside component
area_wall = 0.5  # heat transfer wall area [m2]
ht = 100.0  # heat transfer coef. [W/m2/K]

# define object
gas = ct.Solution('gri30.yaml')
gas.TPX = Tin, p, comp_in
mdot = 1.0 * gas.density

r = ct.IdealGasReactor(gas)
r.volume = 1.0

upstream = ct.Reservoir(gas, name='upstream')
downstream = ct.Reservoir(gas, name='downstream')
m = ct.MassFlowController(upstream, r, mdot=mdot)
v = ct.Valve(r, downstream, K=1.0)

gas.TPX = Toutside, p, comp_outside
outside = ct.Reservoir(gas, name='outside')
wall = ct.Wall(outside, r, U=ht)
wall.area = area_wall

sim = ct.ReactorNet([r])

# solve
sim.advance_to_steady_state()

diagram = sim.draw(print_state=True, species="X")
diagram.view()
