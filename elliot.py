# import modules
import pandas as pd
from pandas import DataFrame
from utils_helper import *

def addImplicant(fileName: str) -> dict:
    '''
    Input: name of file we can read the theory from
    Output: the primeDict with the minterm expressions and boolean representations
    '''
    
    ## Initial Data Processing
    # read by in the truth table/model for the system:
    truthTable = pd.read_excel(fileName)
    truthTable['Term'] = truthTable['Term'].astype(str)
    
    # number of variables is number of columns - 2 (to remove the "terms" column and "f" column)
    numberofVariables = len(truthTable.columns) - 2
    locationOfFirstVar = 1

    # find the minterms that have a truthTable value of 1 or indifferent (x)
    # mintermsValOne = (truthTable.loc[truthTable['f'] == 1])
    # mintermsValX = (truthTable.loc[truthTable['f'] == "x"])
    mintermsValOne = (truthTable.loc[truthTable['output'] == 1])
    mintermsValX = (truthTable.loc[truthTable['output'] == "x"])
    mintermRows = pd.concat([mintermsValOne,mintermsValX])

    # make a dictionary to store the prime implicants
    # keys: combinations of minterms, e.g. "m1,m2,m3,m4"
    # values: binary representation of minterms, e.g. "1-0-"
    primeDict = {}

    ## Initial dictionary
    # make a dictionary that stores the minterm name and the binary representation
    # key is the name of the minterm and the value is the binary representation of the minterm
    mintermDict = {}
    for row in mintermRows.values.tolist():
        mintermDict[row[0]] = row[locationOfFirstVar:numberofVariables+locationOfFirstVar]

    stopLoop = False
    while stopLoop == False:
        # save a copy of the previous mintermDict (will be helpful in extracting solutions)
        prevMintermDict = mintermDict.copy()

        # check each combination of minterms to find which combinations are only different by 1 value
        canCombineSolution = check_differences(mintermDict,numberofVariables)
        # print("canCombineSolution: ", canCombineSolution, "\n")

        # # find the minterms that could not be combined
        uncombinedMinterms = find_uncombined_minterms(canCombineSolution, mintermDict)
        for key in uncombinedMinterms:
            primeDict[key] = prevMintermDict[key]

        # find reduced implicants (that have a dash instead of a binary value)
        combinedMinterms = find_reduced_minterms(canCombineSolution, numberofVariables, mintermDict)

        # if no more minterms can be combined, the algorithm can stop
        if len(combinedMinterms) == 0:
            stopLoop = True

        # re-define the mintermDict
        mintermDict = combinedMinterms.copy()

    return primeDict


def find_conflicts(newEquation, fileName):
    '''
    Find likely conflict candidates using current variable expressions and the theory
    '''
    # Read in the values theoretically assigned to each variable
    actualValsDF = pd.read_excel(fileName)

    # Make a list with the values the variable names
    columnNames = list(actualValsDF.columns)
    columnNames.pop(0)
    columnNames.pop()

    # Make a list with the assigned binary values of the variables
    varAssignments = actualValsDF.values.tolist()[0]
    varAssignments.pop(0)
    varAssignments.pop()

    print(varAssignments)

    # # Dictionary has variables as keys and binary assignments as values
    # assignmentsDict = {}
    # for variable in columnNames:
    #     assignmentsDict[variable] = actualValsDF.iloc[0][variable]

    # Make a dictionary with keys that are the term name and values are the binary representations of the theory
    equationDict = {}
    equationTerms = list(newEquation.split(" + "))
    for termName in equationTerms:
        binaryString = convert_term_to_string(termName, columnNames)
        equationDict[termName] = binaryString

    #Dictionary that shows which terms match the variable assignments
    matchedDict = {}
    for term in equationDict:
        termVals = equationDict[term]
        countMatches = 0
        for i in range(len(termVals)):
            if termVals[i] != varAssignments[i]:
                if termVals[i] == "-":
                    countMatches += 1
            else:
                countMatches += 1
        # if all of the assignments match the equation's term
        if countMatches == len(termVals):
            matchedDict[term] = 1
        else:
            matchedDict[term] = 0

    print(matchedDict)

def get_next_candidate(v_s: list[dict[str, dict[str, str]]]) -> tuple:  

    '''
    Input: all variable candidates
    Output: potential candidates of minimal conflicts to be accepted or rejected by the candidate testor
    '''
    
    #working candidate, initially set to {}
    a_c = {}

    #curent iterative deepening depth, initially set to 1
    d_current = 1

    if d_current <= len(v_s):

        if len(a_c) > 0:

            c_p = a_c

            c_p_prime = c_p

    return 