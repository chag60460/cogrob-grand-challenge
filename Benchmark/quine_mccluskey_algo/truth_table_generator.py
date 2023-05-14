import ttg
from utils import *
        
###################################
# Define part A of thruster problem
thruster_a = QM_Problem()

## Add variables
F1 = thruster_a.add_variable('F1')
P1 = thruster_a.add_variable('P1')

## Add constraints
thruster_a.add_constraint('F1 => P1')
thruster_a.add_constraint('~F1 => ~P1')

## Generate table based on defined variables and constraints (the output is the conjunctive normal form of
## intersection of all the constraints)
table_a = ttg.Truths(thruster_a.get_variables(), thruster_a.get_output())

tableDF_a = table_a.as_pandas()
tableDF_a.to_excel("Thruster_Truth_Table_a.xlsx")




###################################
# Define part B of thruster problem
thruster_b = QM_Problem()

## Add variables
P1 = thruster_b.add_variable('P1')
V1 = thruster_b.add_variable('V1')
P2 = thruster_b.add_variable('P2')
V2 = thruster_b.add_variable('V2')
PV2 = thruster_b.add_variable('PV2')
V3 = thruster_b.add_variable('V3')
PV3 = thruster_b.add_variable('PV3')
P3 = thruster_b.add_variable('P3')

## Add constraints
thruster_b.add_constraint('V1 and P1 => P2')
thruster_b.add_constraint('V1 and ~P1 => ~P2')
thruster_b.add_constraint('~V1 => ~P2')

thruster_b.add_constraint('V2 and P2 => PV2')
thruster_b.add_constraint('V2 and ~P2 => ~PV2')
thruster_b.add_constraint('~V2 => ~PV2')

thruster_b.add_constraint('V3 and P2 => PV3')
thruster_b.add_constraint('V3 and ~P2 => ~PV3')
thruster_b.add_constraint('~V3 => ~PV3')

thruster_b.add_constraint('~PV2 and ~PV3 => ~P3')
thruster_b.add_constraint('PV2 => P3')
thruster_b.add_constraint('PV3 => P3')

## Generate table based on defined variables and constraints
table_b = ttg.Truths(thruster_b.get_variables(), thruster_b.get_output())

tableDF_b = table_b.as_pandas()
tableDF_b.to_excel("Thruster_Truth_Table_b.xlsx")





###################################
# Define part C of thruster problem
thruster_c = QM_Problem()

## Add variables
P3 = thruster_c.add_variable('P3')
R1 = thruster_c.add_variable('R1')
T1 = thruster_c.add_variable('T1')

## Add constraints
thruster_c.add_constraint('R1 and P3 => T1')
thruster_c.add_constraint('R1 and ~P3 => ~T1')
thruster_c.add_constraint('~R1 => ~T1')


## Generate table based on defined variables and constraints
table_c = ttg.Truths(thruster_c.get_variables(), thruster_c.get_output())

tableDF_c = table_c.as_pandas()
tableDF_c.to_excel("Thruster_Truth_Table_c.xlsx")