# import statements
import pandas as pd
from utils_helper import *

############################################# End of Helper Functions #############################################

#### FIND PRIME IMPLICANT Chart ########
## Input: name of file we can read the theory from
## Output: tuple of (originalEquation, mintermsValOne, primeDict)
## Where originalEquation is the original theory expression, mintermsValOne are all the minterms that have an output of one and the primeDict has the minterm expressions and bollean representations
def find_prime_implicants(fileName):
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

    originalEquation = binary_rep_to_equation(truthTable, mintermDict)

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
        # print("uncombinedMinterms: ", uncombinedMinterms, "\n")

        # find reduced implicants (that have a dash instead of a binary value)
        combinedMinterms = find_reduced_minterms(canCombineSolution, numberofVariables, mintermDict)
        # print("combinedMinterms: ", combinedMinterms, "\n")

        # if no more minterms can be combined, the algorithm can stop
        if len(combinedMinterms) == 0:
            stopLoop = True

        # re-define the mintermDict
        mintermDict = combinedMinterms.copy()
        # print("MINTERM DICT: ", mintermDict,"\n")

    return(originalEquation, mintermsValOne, primeDict)

####### Use Prime Implicant Chart to Make Shortened Equation ########
## Input: File name that has the theory
## Output: (Original theory expression, new theory expression)
def find_min_expression(fileName):

    ## Get information from prime implicant chart
    (originalEquation, mintermsValOne, primeDict) = find_prime_implicants(fileName)
    numberofVariables = len(mintermsValOne.columns) - 2
    # make a dictionary to store the final implicants that will be used to represent the theory
    # keys: combinations of minterms, e.g. "m1,m2,m3,m4"
    # values: binary representation of minterms, e.g. "1-0-"
    finalDict = {}

    # Find the terms that output 1 (excluding "don't care" terms). These will be the column headers
    oneMinterms = mintermsValOne['Term'].to_list()

    # Count how often a minterm is covered by the solution (i.e. number of check marks per column)
    countList = count_minterms(oneMinterms,primeDict)

    # When a minterm only shows up once, make sure the implicant that includes it is added to the prime implicant dictionary
    # Make a list of minterms that only show up once
    uniqueMintermsList = []
    for i in range(len(oneMinterms)):
        if countList[i] == 1:
            uniqueMintermsList.append(oneMinterms[i])

    # Iterate through the implicants. If one has a minterm that only shows up once, add it to the solution set
    for implicant in primeDict.keys():
        listMinNames = list(implicant.split(","))
        for indvMinName in listMinNames:
            if indvMinName in uniqueMintermsList:
                finalDict[implicant] = primeDict[implicant]

    # Check which minterms were not covered by the unique implicants
    unincludedMinterms = unincluded_minterms(oneMinterms,finalDict)

    ## While there are minterms that have not yet been included, add more implicants to the prime implicant list until they're all covered
    while len(unincludedMinterms) > 0:
        # Count dictionary will have keys be the implicants and values be the count of missing minterms covered
        countDict = primeDict.copy()
        for implicant in primeDict:
            countDict[implicant] = 0

        # Count how many missing minterms each implicant will cover
        for implicant in primeDict:
            listMinNames = list(implicant.split(","))
            for term in listMinNames:
                for minterm in unincludedMinterms:
                    if term == minterm:
                        countDict[implicant] += 1

        # Add the implicant that covers the most missing minterms
        implicantToAdd = max(countDict, key = countDict.get)
        finalDict[implicantToAdd] = primeDict[implicantToAdd]

        # Re-evaluate which minterms are missing
        unincludedMinterms = unincluded_minterms(oneMinterms,finalDict)

    ## Write an equation that represents the solution
    newEquation = binary_rep_to_equation(mintermsValOne, finalDict)

    return(originalEquation, newEquation)

### find likely conflict candidates using current variable expressions and the theory
def find_conflicts(newEquation, fileName):

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

