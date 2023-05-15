from .elliot import *
from .set_up import *
from tqdm import tqdm

def find_prime_implicants_elliot(p: Problem, Vs: list):
    minimal_conflicts = []
    conflicts = []
    satisfiable = []
    prime_implicants = []
    implicants = []
    
    #SAT Solver
    sat = SATSolver(p)
    print('sat',sat)

    #Derive all_domains
    all_domains = get_domain(p, Vs)
    print('all_domains',all_domains)

    #Derive reduced_set
    reduced_set = derive_reduced_set(all_domains)
    print('reduced_set',reduced_set)

    #Get children
    children = get_children(reduced_set)
    print('children',children)

    #Find Prime Implicants
    for assignment in tqdm(reduced_set):
        candidate = frozenset([p.get_variable(a.var.__str__()).get_assignment(a.val) for a in assignment])
        #print('candidate',candidate)
        
        # prunes (doesn't test candidates that are children of prime implicants)
        if any(S.issubset(candidate) for S in prime_implicants):
            implicants.append(candidate)

        # prunes (doesn't test candidates that are children of prime implicants)
        elif any(S.issubset(candidate) for S in minimal_conflicts):
            conflicts.append(candidate)
        
        # check if candidate is a prime implicant for nodes that have children
        elif candidate in children and is_valid_benchmark(p, candidate, sat, children, reduced_set) and \
            not any(S.issubset(candidate) for S in prime_implicants):
                prime_implicants.append(candidate)

        # check if candidate is a prime implicant for nodes that don't have children
        elif len(candidate) == len(Vs) and \
            sat.check_consistency(candidate)[0] and \
            not any(S.issubset(candidate) for S in prime_implicants):
                prime_implicants.append(candidate)

        elif not sat.check_consistency(candidate)[0] and \
            not any(S.issubset(candidate) for S in minimal_conflicts):
                minimal_conflicts.append(candidate)

        elif sat.check_consistency(candidate)[0]:
            satisfiable.append(candidate)

    return {'prime_implicants': prime_implicants, 'minimal_conflicts': minimal_conflicts}