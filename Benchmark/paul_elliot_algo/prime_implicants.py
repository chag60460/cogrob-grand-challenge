from .elliot import *
from .set_up import *

def find_prime_implicants_elliot(p: Problem, Vs: list):
    minimal_conflicts = []
    conflicts = []
    satisfiable = []
    prime_implicants = []
    implicants = []
    
    #SAT Solver
    sat = SATSolver(p)

    #Derive all_domains
    all_domains = get_domain(p, Vs)

    #Derive reduced_set
    reduced_set = derive_reduced_set(all_domains)

    #Get children
    children = get_children(reduced_set)

    #Find Prime Implicants
    for assignment in reduced_set:
        candidate = frozenset([p.get_variable(a.var.__str__()).get_assignment(a.val) for a in assignment])
        
        if candidate in children and is_valid_benchmark(p, candidate, sat, children) and not any(S.issubset(candidate) for S in prime_implicants):
            prime_implicants.append(candidate)

        elif len(candidate) == len(Vs) and \
            sat.check_consistency(candidate)[0] and \
            not any(S.issubset(candidate) for S in prime_implicants):
                prime_implicants.append(candidate)

        elif not sat.check_consistency(candidate)[0] and \
            not any(S.issubset(candidate) for S in minimal_conflicts):
                minimal_conflicts.append(candidate)

        elif any(S.issubset(candidate) for S in prime_implicants):
            implicants.append(candidate)

        elif any(S.issubset(candidate) for S in minimal_conflicts):
            conflicts.append(candidate)

        elif sat.check_consistency(candidate)[0]:
            satisfiable.append(candidate)

    return prime_implicants