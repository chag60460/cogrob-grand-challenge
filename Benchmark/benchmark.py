import time
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
variable_list = p.variables

############################## Thruster Example - Placeholder ################################
thruster = Problem()

# Define the variables for the mini thruster problem with variables: T1, R1, and P3. Returns a Variable object.
# Thrust: T1
T1 = thruster.add_variable('thruster', type='finite_domain', domain=['thrust', 'nothrust'])
# Thruster: R1
R1 = thruster.add_variable('runthruster', type='finite_domain', domain=['on', 'off'])
# Pressure before the thruster: P3
P3 = thruster.add_variable('pressure', type='finite_domain', domain=['high', 'low'])

# Add the theory / problem constraints.
# The thruster only outputs thrust when it is on and when the input from P3 is high
thruster.add_constraint('runthruster=on & pressure=high => thruster=thrust')
thruster.add_constraint('runthruster=on & pressure=low => thruster=nothrust')
thruster.add_constraint('runthruster=off => thruster=nothrust')

# Prints out constraints nicely in LaTeX, so you can check them.
display_constraints(thruster)

# Define SAT for future use
sat = SATSolver(thruster)

thruster_model = {
    frozenset([T1.get_assignment('thrust')]) : {
        frozenset([T1.get_assignment('thrust'), R1.get_assignment('on')]) : {
            frozenset([T1.get_assignment('thrust'), R1.get_assignment('on'), P3.get_assignment('high')]) : {},
            frozenset([T1.get_assignment('thrust'), R1.get_assignment('on'), P3.get_assignment('low')]) : {},
            },
        frozenset([T1.get_assignment('thrust'), R1.get_assignment('off')]) : {
            frozenset([T1.get_assignment('thrust'), R1.get_assignment('off'), P3.get_assignment('high')]) : {},
            frozenset([T1.get_assignment('thrust'), R1.get_assignment('off'), P3.get_assignment('low')]) : {},
            },
        frozenset([T1.get_assignment('thrust'), P3.get_assignment('high')]) : {},
        frozenset([T1.get_assignment('thrust'), P3.get_assignment('low')]) : {},
        },
    
    frozenset([T1.get_assignment('nothrust')]) : {
        frozenset([T1.get_assignment('nothrust'), R1.get_assignment('on')]) : {
            frozenset([T1.get_assignment('nothrust'), R1.get_assignment('on'), P3.get_assignment('high')]) : {},
            frozenset([T1.get_assignment('nothrust'), R1.get_assignment('on'), P3.get_assignment('low')]) : {},
            },
        frozenset([T1.get_assignment('nothrust'), R1.get_assignment('off')]) : {
            frozenset([T1.get_assignment('nothrust'), R1.get_assignment('off'), P3.get_assignment('high')]) : {},
            frozenset([T1.get_assignment('nothrust'), R1.get_assignment('off'), P3.get_assignment('low')]) : {},
            },
        frozenset([T1.get_assignment('nothrust'), P3.get_assignment('high')]) : {},
        frozenset([T1.get_assignment('nothrust'), P3.get_assignment('low')]) : {},
        },
    
    frozenset([R1.get_assignment('on')]) : {
            frozenset([R1.get_assignment('on'), P3.get_assignment('high')]) : {},
            frozenset([R1.get_assignment('on'), P3.get_assignment('low')]) : {},
            },
        frozenset([R1.get_assignment('off')]) : {
            frozenset([R1.get_assignment('off'), P3.get_assignment('high')]) : {},
            frozenset([R1.get_assignment('off'), P3.get_assignment('low')]) : {},
            },
    
    frozenset([P3.get_assignment('high')]) : {},
    
    frozenset([P3.get_assignment('low')]) : {},
}

candidate1 = frozenset([T1.get_assignment('thrust')])
candidate2 = frozenset([T1.get_assignment('nothrust')])
candidate4 = frozenset([R1.get_assignment('off')])
candidate1A = frozenset([T1.get_assignment('thrust'), R1.get_assignment('on')])
candidate1B = frozenset([T1.get_assignment('thrust'), R1.get_assignment('off')])
candidate2A = frozenset([T1.get_assignment('nothrust'), R1.get_assignment('on')])
candidate2B = frozenset([T1.get_assignment('nothrust'), R1.get_assignment('off')])

candidateList = [
    (candidate1, thruster_model[candidate1]),
    (candidate2, thruster_model[candidate2]),
    (candidate4, thruster_model[candidate4]),
    (candidate1A,thruster_model[candidate1][candidate1A]),
    (candidate1B,thruster_model[candidate1][candidate1B]),
    (candidate2A,thruster_model[candidate2][candidate2A]),
    (candidate2B,thruster_model[candidate2][candidate2B]),
]

############################## Benchmark Algorithms #########################################
def quine_mccluskey(fileName: str) -> tuple:
    start_time = time.time()
    find_prime_implicants(fileName)
    print(f"quine_mccluskey {time.time() - start_time}, to run")

def paul_elliot(sat: SATSolver, candidateList: list):
    start_time = time.time()
    prime_implicate_finder(sat, candidateList)
    print(f"paul_elliot {time.time() - start_time}, to run")

quine_mccluskey('Problem_Theory_v1.xlsx')
paul_elliot(sat, candidateList)