import ttg

# Problem class for the QM algorithm
class QM_Problem():
    def __init__(self):
        # Useful datastructures
        self.variables = []
        self.main_variables = []
        self.intermediate_variables = []
        self.constraints = []
        self.operators = ['not', '-', '~', 'or', 'nor', 'xor', '!=', 'and', 'nand', '=>', 'implies', '=']

    def add_variable(self, name, intermediate=False):
        if name in self.variables:
            raise Exception("Variable already exists!")
        
        if not isinstance(name, str):
            raise Exception("Variables must be declared as strings")
        
        if not intermediate:
            self.variables.append(name)
            self.main_variables.append(name)
        else:
            self.variables.append(name)
            self.intermediate_variables.append(name)

        return name
    
    def add_constraint(self, expression):
        if expression in self.constraints:
            raise Exception("Constraint already exists!")
        
        if not isinstance(expression, str):
            raise Exception("Constraints must be declared as strings")
        
        parsed = expression.replace('~', '~ ').replace('-', '- ').replace('(','').replace(')','').split(' ')

        if any(not ((term in self.variables) or (term in self.operators)) for term in parsed):
            raise Exception("Constraints must be made up of valid variables and operators")
        
        self.constraints.append(expression)

        return expression
    
    def get_variables(self):
        return self.variables
    
    def get_main_variables(self):
        return self.main_variables
    
    def get_intermediate_variables(self):
        return self.intermediate_variables
    
    def get_constraints(self):
        return self.constraints
    
    def get_output(self):
        if len(self.constraints) == 0:
            raise Exception("Requires at least one constraints to get an output")
        elif len(self.constraints) == 1:
            return self.constraints
        else:
            return ['(' + ') and ('.join(self.constraints) + ')']
        


# Define thruster problem
p = QM_Problem()

## Add variables
#F1 = p.add_variable('F1')
P1 = p.add_variable('P1')
V1 = p.add_variable('V1')
P2 = p.add_variable('P2', intermediate = True)
V2 = p.add_variable('V2')
PV2 = p.add_variable('PV2', intermediate = True)
V3 = p.add_variable('V3')
PV3 = p.add_variable('PV3', intermediate = True)
P3 = p.add_variable('P3')
#R1 = p.add_variable('R1', intermediate = True)
#T1 = p.add_variable('T1', intermediate = True)


## Add constraints
#p.add_constraint('F1 => P1')
#p.add_constraint('~F1 => ~P1')

p.add_constraint('V1 and P1 => P2')
p.add_constraint('V1 and ~P1 => ~P2')
p.add_constraint('~V1 => ~P2')

p.add_constraint('V2 and P2 => PV2')
p.add_constraint('V2 and ~P2 => ~PV2')
p.add_constraint('~V2 => ~PV2')

p.add_constraint('V3 and P2 => PV3')
p.add_constraint('V3 and ~P2 => ~PV3')
p.add_constraint('~V3 => ~PV3')

p.add_constraint('~PV2 and ~PV3 => ~P3')
p.add_constraint('PV2 => P3')
p.add_constraint('PV3 => P3')

#p.add_constraint('R1 and P3 => T1')
#p.add_constraint('R1 and ~P3 => ~T1')
#p.add_constraint('~R1 => ~T1')


## Generate table based on defined variables and constraints (the output is the conjunctive normal form of
## intersection of all the constraints)

print(p.get_main_variables())

print(p.get_output())

print(p.get_intermediate_variables())

print(p.get_intermediate_variables() + p.get_output())

print(ttg.Truths(p.get_main_variables(), p.get_intermediate_variables() + p.get_output()))

#table = ttg.Truths(p.get_main_variables(), p.get_output())

#tableDF = table.as_pandas()
#tableDF.to_excel("Thruster_Truth_Table.xlsx")