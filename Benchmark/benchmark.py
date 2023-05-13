from paul_elliot_algo.prime_implicate import *
from quine_mccluskey_algo.quine_mccluskey import *
from src.propositional_state_logic import *
from src.sat_solver import *

############################### Problem Setup ##############################################
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

############################### SAT Setup ##############################################
sat = SATSolver(p)

############################### Variable Setup ##############################################
variable_list = p.get_decision_variables()

def quine_mccluskey(fileName: str) -> tuple:
    find_prime_implicants(fileName)

def paul_elliot(sat: SATSolver, variable_list: list):
    print(prime_implicate_finder(sat, variable_list))

quine_mccluskey('Problem_Theory_v1.xlsx')
paul_elliot(sat, variable_list)