from src.propositional_state_logic import *
from src.sat_solver import *
from src.utils import *
from copy import deepcopy

########################################### Problem Setup ##############################################
p = Problem()

# Define the variables above. Returns a Variable object.
F1 = p.add_variable('F1', type='binary')
P1 = p.add_variable('P1', type='binary')
V1 = p.add_variable('V1', type='binary')
P2 = p.add_variable('P2', type='binary')
V2 = p.add_variable('V2', type='binary')
PV2 = p.add_variable('PV2', type='binary')
V3 = p.add_variable('V3', type='binary')
PV3 = p.add_variable('PV3', type='binary')
P3 = p.add_variable('P3', type='binary')
R1 = p.add_variable('R1', type='binary')
T1 = p.add_variable('T1', type='binary')

# Add the word problem constraints.
p.add_constraint('F1 => P1')
p.add_constraint('~F1 => ~P1')

p.add_constraint('V1 & P1 => P2')
p.add_constraint('V1 & ~P1 => ~P2')
p.add_constraint('~V1 => ~P2')

p.add_constraint('V2 & P2 => PV2')
p.add_constraint('V2 & ~P2 => ~PV2')
p.add_constraint('~V2 => ~PV2')

p.add_constraint('V3 & P2 => PV3')
p.add_constraint('V3 & ~P2 => ~PV3')
p.add_constraint('~V3 => ~PV3')

p.add_constraint('~PV2 & ~PV3 => ~P3')
p.add_constraint('PV2 => P3')
p.add_constraint('PV3 => P3')

p.add_constraint('R1 & P3 => T1')
p.add_constraint('R1 & ~P3 => ~T1')
p.add_constraint('~R1 => ~T1')

#Establish Variables
Vs = ['T1', 'R1', 'P3']
Vs1 = ['F1', 'P1']
Vs2 = ['P1', 'V1', 'V2', 'V3', 'P3']
