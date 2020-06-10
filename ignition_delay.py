import numpy as np
import matplotlib.pyplot as plt
import cantera as ct

# condition
temp = 1000.0
p = 1.3e6
phi = 1.0

# define gas state
gas = ct.Solution('LLNL_heptane_160.cti')
gas.TP = temp, p
gas.set_equivalence_ratio(phi, 'nc7h16', 'o2:1.0, n2:3.76')
states = ct.SolutionArray(gas, extra=['t'])

# define reactor
r = ct.IdealGasReactor(contents=gas, name='Batch Reactor')
sim = ct.ReactorNet([r])

# time condition
tend = 0.1  # end time
dt = 1.0e-6 # time step

# time loop
for time in np.arange(0, tend, dt):
    sim.advance(time)
    states.append(r.thermo.state, t=time)

# ignition delay time
time_igd = states.t[np.argmax(np.diff(states.T))]
print('\n Ignition Delay Time: {:.3e} micro sec'.format(time_igd * 1e6))

#plot
plt.plot(states.t, states.T)
plt.xlim(0, 0.01)
plt.xlabel('Time [sec]')
plt.ylabel('Temperature [K]')
plt.show()
