def is_conflict(sat, candidate):
    return not sat.check_consistency(candidate)[0]

def get_all_children(d):
    for key, value in d.items():
        yield key
        if isinstance(value, dict):
            yield from get_all_children(value)

def is_valid(candidate, sat, thruster_model_children):
    # list of all the following partial assignments
    childCandidateList = list(get_all_children(thruster_model_children))
    for child in childCandidateList:
        if is_conflict(sat, child):
            return False
    return True

def is_unsatisfiable(candidate, sat, thruster_model_children):
    # list of all the following partial assignments
    childCandidateList = list(get_all_children(thruster_model_children))
    
    if is_conflict(sat, candidate):
        return True
    
    for child in childCandidateList:
        if not is_conflict(sat, child): # if one of the children is consistent
            return False
    return True