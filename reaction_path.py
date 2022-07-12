"""
Reaction path diagram
"""

import os
import sys
import cantera as ct

# Define a gas mixture
gas = ct.Solution('gri30.yaml')
gas.TPX = 1500.0, ct.one_atm, 'CH4:0.25, O2:1, N2:3.76'
r = ct.IdealGasReactor(gas)
net = ct.ReactorNet([r])
T = r.T
while T < 1900:
    net.step()
    T = r.T

# Define the element in the reaction path
element = 'N'

# Create reaction path diagram
diagram = ct.ReactionPathDiagram(gas, element)
diagram.title = 'Reaction path diagram following {0}'.format(element)
diagram.label_threshold = 0.01

dot_file = 'reaction_path.dot'
img_file = 'reaction_path.png'

diagram.write_dot(dot_file)
print(diagram.get_data())

os.system('dot {0} -Tpng -o{1} -Gdpi=300'.format(dot_file, img_file))
