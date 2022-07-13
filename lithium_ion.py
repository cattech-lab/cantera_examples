import cantera as ct
print('Runnning Cantera version: ' + ct.__version__)

import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# define object
input_file = 'lithium_ion_battery.yaml'
anode = ct.Solution(input_file, 'anode')
cathode = ct.Solution(input_file, 'cathode')
elde = ct.Solution(input_file, 'electron')
elyte = ct.Solution(input_file, 'electrolyte')
anode_interface = ct.Interface(input_file, 'edge_anode_electrolyte', [anode, elde, elyte])
cathode_interface = ct.Interface(input_file, 'edge_cathode_electrolyte', [cathode, elde, elyte])

# lithium mole fractions
X_Li_an = np.arange(0.005, 0.995, 0.02)
X_Li_ca = 1. - X_Li_an

# I_app = 0: Open circuit current
I_app = 0.

# At zero current, electrolyte resistance is irrelevant:
R_elyte = 0.

# Temperature and pressure
T = 300 # [K]
P = ct.one_atm # [Pa]
F = ct.faraday # Faraday's constant
S_ca = 1.1167 # [m2] Cathode total active material surface area
S_an = 0.7824 # [m2] Anode total active material surface area
phases = [anode, elde, elyte, cathode, anode_interface, cathode_interface]
for ph in phases:
    ph.TP = T, P

# function of anode current difference
def anode_curr(phi_l,I_app,phi_s,X_Li_an):
    # Set the active material mole fraction
    anode.X = 'Li[anode]:' + str(X_Li_an) + ', V[anode]:' + str(1 - X_Li_an)

    # Set the electrode and electrolyte potential
    elde.electric_potential = phi_s
    elyte.electric_potential = phi_l

    # Get the net product rate of electrons in the anode (per m2 interface)
    r_elec = anode_interface.get_net_production_rates(elde)

    anCurr = r_elec*ct.faraday*S_an
    diff = I_app + anCurr
    
    return diff

# function of cathode current difference
def cathode_curr(phi_s,I_app,phi_l,X_Li_ca):
    # Set the active material mole fractions
    cathode.X = 'Li[cathode]:' + str(X_Li_ca) + ', V[cathode]:' + str(1 - X_Li_ca)

    # Set the electrode and electrolyte potential
    elde.electric_potential = phi_s
    elyte.electric_potential = phi_l
    
    # Get the net product rate of electrons in the cathode (per m2 interface)
    r_elec = cathode_interface.get_net_production_rates(elde)
    
    caCurr = r_elec*ct.faraday*S_an
    diff = I_app - caCurr
    
    return diff

# solve
E_cell_kin = np.zeros_like(X_Li_ca)
for i,X_an in enumerate(X_Li_an):
    #Set anode electrode potential to 0:
    phi_s_an = 0
    E_init = 3.0
   
    # electrolyte potential at anode interface
    phi_l_an = fsolve(anode_curr,E_init,args=(I_app, phi_s_an, X_an))
    
    # electrolyte potential at cathode interface
    phi_l_ca = phi_l_an + I_app*R_elyte
    
    # cathode electrode potential
    phi_s_ca = fsolve(cathode_curr,E_init,args=(I_app, phi_l_ca, X_Li_ca[i]))
    
    # Calculate cell voltage
    E_cell_kin[i] = phi_s_ca - phi_s_an

# plot
plt.plot(100*X_Li_ca, E_cell_kin, color='b', linewidth=2.5)
plt.xlabel('Li Fraction in Cathode [%]')
plt.ylabel('Open Circuit Voltage [V]')
plt.xlim(0, 100)
plt.ylim(2.5, 5)
plt.grid(True)
plt.show()
