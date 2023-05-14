import itertools

########################################### Helper Functions #######################################
def convert_term_to_string(termName, variableNames):
    '''
    Converts an equation's term (e.g. A'BC') to a binary boolean representation
    @Input: Term name and names of the variables
    @Output: list with the binary variable assignments (e.g. [0, 1, 0, -"])
    '''
    binaryList = []
    termCharacters = [*termName] #turn the term into a list of characters e.g. [A, ', B, C, ']

    for variable in variableNames:
        # When variable is missing it should be a "-" in the binary assignment
        if variable not in termCharacters:
            binaryList.append("-")
        else:
            charSpot = termCharacters.index(variable)
            # if the character is last, that means it can't be a "NOT":
            if charSpot == len(termCharacters) - 1:
                binaryList.append(1)
            else:
                # If variable is a "NOT" e.g. A'
                if termCharacters[charSpot + 1] == "'":
                    binaryList.append(0)
                else:
                    binaryList.append(1)
    return binaryList

def check_differences(mintermDict, numberofVariables):
    '''
    Function that checks which variable assignments are different by 1 value
    Inputs: dictionary with keys that are names of minterms and values that are binary representations of the minterms and the number of variables in each minterm
    Output: list of lists. Each sublist is a pair of minterms that can be combined
    '''
    canCombineSolution = []
    for minterm1 in mintermDict.keys():
        for minterm2 in mintermDict.keys():
            if minterm1 != minterm2:
                # compare the binary representations for 2 minterms and count how many values they share
                numMatchingVals = 0
                for i in range(numberofVariables):
                    if mintermDict[minterm1][i] == mintermDict[minterm2][i]:
                        numMatchingVals += 1
                # if minterms only vary by 1 value, they can be combined
                if numMatchingVals == numberofVariables - 1:
                    # only add pair that is not already in the list of matches
                    if [minterm1,minterm2] not in canCombineSolution and [minterm2,minterm1] not in canCombineSolution:
                        canCombineSolution.append([minterm1,minterm2])
    return canCombineSolution

def find_uncombined_minterms(canCombineSolution, mintermDict):
    '''
    Function that finds the minterms that cannot be combined
    Input: list of lists where each sublist is a pair of minterms that can be combined and dictionary with minterm name and binary representation
    Output: list of minterms that cannot be combined
    '''
    uncombinedMinterms = []
    #list of all the minterms that can be combined
    mintermsInCombinedList = list(itertools.chain(*canCombineSolution))
    # print("MINTERMS IN COMBINED LIST: ", mintermsInCombinedList)
    for minterm in mintermDict.keys():
        if minterm not in mintermsInCombinedList:
            uncombinedMinterms.append(minterm)
    return uncombinedMinterms

def find_reduced_minterms(canCombineSolution, numberofVariables, mintermDict):
    '''
    Function: find reduced implicants (that have a dash instead of a binary value)
    Input: list of lists where each sublist is a pair of minterms that can be combined, the number of variables in each minterm, and dictionary with minterm name and binary representation
    Output: Dictionary that keys: the names of combined minterms  and the values: the binary representation of the combined minterms
    '''
    combinedMinterms = {}
    for pair in canCombineSolution:
        minterm1 = mintermDict[pair[0]]
        minterm2 = mintermDict[pair[1]]
        newMinterm = []
        # print("MINTERM 1: ", minterm1)
        # print("MINTERM 2: ", minterm2)
        # print("========================")
        # constructing the new minterm value by value
        for i in range(numberofVariables):
            if minterm1[i] != minterm2[i]:
                newMinterm.append("-")
            else:
                newMinterm.append(minterm1[i])
        newMintermLabel = pair[0] + "," + pair[1]
        #print(newMintermLabel)
        if newMinterm not in combinedMinterms.values():
            combinedMinterms[newMintermLabel] = newMinterm

    return combinedMinterms

def binary_rep_to_equation(truthTable, mintermDict):
    '''
    convert a dictionary containing binarry representations to a formula
    dictionary has keys that are the names of the minterms and values that are the binary representations
    output: string that represents the final equation, e.g. A'B' + ACDE
    '''
    # Make a list with just the variable names
    columnNames = list(truthTable.columns)
    columnNames.pop(0)
    columnNames.pop()

    equationString = ""

    numTerms = 0
    for minNames, binRep in mintermDict.items():
        numTerms += 1
        for i in range(len(binRep)):
            # if the value is a 0, the equation has the not of a variable, e.g. B'
            if binRep[i] == 0:
                equationString = equationString + columnNames[i] + "'"
            # if the value is a 1, the equation has the variable, e.g. B
            elif binRep[i] == 1:
                equationString = equationString + columnNames[i]
            # if the value is "-", that means the variable is not included in the statement
            else:
                continue
        # add a "+" after each term of the equaation, except the last term
        if numTerms != len(mintermDict):
            equationString = equationString + " + "

    return equationString

def count_minterms(oneMinterms,primeDict):
    '''
    Count how often a minterm is included in a dictionary of implicants
    Input 1: Dictionary where the keys are implicant names and the values are binary representations of minterms
    Input 2: list with the minterms we want to count
    Output: list with the count of each minterm (the indexes line up)
    '''
    countList = [0]*len(oneMinterms)
    for i in range(len(oneMinterms)):
        for allMinNames in primeDict.keys():
            # make a list where each element is the name of a minterm
            listMinNames = list(allMinNames.split(","))
            for indvMinName in listMinNames:
                # if the solution covers that minterm, add to the count
                if indvMinName == oneMinterms[i]:
                    countList[i] += 1

    return(countList)

def unincluded_minterms(oneMinterms,finalDict):
    '''
    Count unincluded minterms (minterms that are not covered by the prime implicants)
    Input 1: Dictionary where the keys are implicant names and the values are binary representations of minterms
    Input 2: Dictionary that has the current prime implicants that will be included in the solution
    Output: list of minterms that are not included by the solution set
    '''
    # Check which minterms were not covered by the unique implicants
    # The minterms that are not included yet will have a count of 0
    countOfCurrentMinterms = count_minterms(oneMinterms,finalDict)

    # Make a list of the minterms that have not been included yet
    unincludedMinterms = []
    for i in range(len(oneMinterms)):
        if countOfCurrentMinterms[i] == 0:
            unincludedMinterms.append(oneMinterms[i])

    return unincludedMinterms


####### QM Problem class for the QM algorithm

class QM_Problem():
    def __init__(self):
        # Useful datastructures
        self.variables = []
        self.constraints = []
        self.operators = ['not', '-', '~', 'or', 'nor', 'xor', '!=', 'and', 'nand', '=>', 'implies', '=']

    def add_variable(self, name):
        if name in self.variables:
            raise Exception("Variable already exists!")
        
        if not isinstance(name, str):
            raise Exception("Variables must be declared as strings")
        
        self.variables.append(name)

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
    
    def get_constraints(self):
        return self.constraints
    
    def get_output(self):
        if len(self.constraints) == 0:
            raise Exception("Requires at least one constraints to get an output")
        elif len(self.constraints) == 1:
            return self.constraints
        else:
            return ['(' + ') and ('.join(self.constraints) + ')']