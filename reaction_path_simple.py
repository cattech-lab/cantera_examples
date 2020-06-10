"""
Reaction path diagram
"""

import os
import sys
import cantera as ct

# Define a gas mixture
gas = ct.Solution('gri30.xml')
gas.TPX = 1500.0, ct.one_atm, 'CH4:0.25, O2:1, N2:3.76'

# Define the element in the reaction path
element = 'N'

# Create reaction path diagram
diagram = ct.ReactionPathDiagram(gas, element)
diagram.title = 'Reaction path diagram following {0}'.format(element)
diagram.label_threshold = 0.01

dot_file = 'reaction_path_simple.dot'
img_file = 'reaction_path_simple.png'

diagram.write_dot(dot_file)
print(diagram.get_data())

os.system('dot {0} -Tpng -o{1} -Gdpi=300'.format(dot_file, img_file))
