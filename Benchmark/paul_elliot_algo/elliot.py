import itertools
from copy import deepcopy
from src.sat_solver import *

############################################## Nodes ##################################################
def findsubsets(s, n):
    return (list(tup) for tup in itertools.combinations(s, n))

def get_nodes(variable_list):
    nodes = []

    for i in range(len(variable_list)+1):
        for n in findsubsets(variable_list, i):
            nodes.append(n)

    return nodes

############################################## Domains ##################################################
def get_domain(p: Problem, variable_list):
    all_domains = []
    
    for v in variable_list:
        var = p.get_variable(v)
        for a in list(var.domain):
            all_domains.append(var.get_assignment(a))

    return all_domains

######################################## Derive Reduced Set ##################################################
def derive_reduced_set(all_domains): 
    full_set = get_nodes(all_domains)
    
    reduced_set = []
    
    for v in full_set:
        if len(v) == len(set([a.var for a in v])):
            #reduced_set.append([a.__str__() for a in v])
            reduced_set.append(v)

    return reduced_set

######################################## Derive Tree from Reduced Set ##################################################
def list_tree(reduced_set, n):
    new_nodes = deepcopy(reduced_set)
    if n in new_nodes:
        new_nodes.remove(n)

    a = []
    a.append(n)

    if new_nodes == [] or [j for j in new_nodes if n != j and [v.__str__() for v in n] == [v.__str__() for v in j[:len(n)]] and len(j) == len(n)+1] == []:
        a.append([])
        
    else:
        a.append([list_tree([k for k in new_nodes if k != j], j) for j in new_nodes if n != j and [v.__str__() for v in n] == [v.__str__() for v in j[:len(n)]] and len(j) == len(n)+1])
    
    return a

####################################### Get Children #######################################################
def get_children(reduced_set):
    children = {}

    for x in reduced_set:
        for y in reduced_set:
            if x != [] and [v.__str__() for v in x] != [v.__str__() for v in y] and all(a in [v.__str__() for v in y] for a in [v.__str__() for v in x]):
                if frozenset(x) not in children:
                    children[frozenset(x)] = []
                    
                children[frozenset(x)].append(frozenset(y))

    return children

######################################## Traverse Tree ##################################################
def traverse(tree):
    if tree != []:
        if isinstance(tree, list) and len(tree) > 1:
            if not isinstance(tree[0], list):
                yield tree
            else:
                for value in tree:
                    #print('value',value, isinstance(value, list))
                    for subvalue in traverse(value):
                        yield subvalue
        else:
            yield tree


###################################### Check Satisfiablility ################################################
def is_satisfiable(p: Problem, sat: SATSolver, tree: list):
    satisfiable = []

    for assignment in traverse(tree):
        candidate = frozenset([p.get_variable(a.var.__str__()).get_assignment(a.val) for a in assignment])
        if sat.check_consistency(candidate)[0] == True:
            satisfiable.append(candidate)
    
    return satisfiable

###################################### Check Unsatisfiablility ################################################
def is_conflict(p: Problem, sat: SATSolver, tree: list):
    conflicts = []
    
    for assignment in traverse(tree):
        candidate = frozenset([p.get_variable(a.var.__str__()).get_assignment(a.val) for a in assignment])
        if not sat.check_consistency(candidate)[0]:
            conflicts.append(candidate)
    
    return conflicts

###################################### Check Validity ################################################
def is_valid_benchmark(p, candidate, sat, children):
    childCandidateList = children[(candidate)]
    for child in childCandidateList:
        if is_conflict(p, sat, child):
            return False
    return True