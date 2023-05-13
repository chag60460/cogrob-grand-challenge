from .test_validity import *

def prime_implicate_finder(sat, candidateList):
    ## sat represents the theory behind the represented model
    ## CandidateList: List of Tuples (candidate, model_children), 
        # where the candidate is the item to be tested and 
        # model_children is a dictionary holding the children of the given candidate
    ## generatorAdditions: add candidate to generatorAdditions list when it should go to the generator
    ## convertToImplicate: add candidate to the convertToImplicateList when it needs to be converted to an implicate before being passed to the generator
    ## solutions: add candidate to the solutions list when a candidate is a minimal conflict
    ### Function should return a tuple in the format (generatorAdditions, convertToImplicate, solutions)
    
    generatorAdditions = []
    convertToImplicate = []
    solutions = []
    
    for candidateTuple in candidateList:
        candidate = candidateTuple[0]
        model_children = candidateTuple[1]
        
        if is_valid(candidate, sat, model_children):
            generatorAdditions.append(candidate)
        elif is_unsatisfiable(candidate, sat, model_children):
            solutions.append(candidate)
        else: #candidate is satisfiable
            convertToImplicate.append(candidate)
    
    return (generatorAdditions, convertToImplicate, solutions)