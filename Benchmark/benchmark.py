import time
from paul_elliot_algo.set_up import *
from paul_elliot_algo.prime_implicants import *
from quine_mccluskey_algo.quine_mccluskey import *
from quine_mccluskey_algo.truth_table_generator import *
from src.propositional_state_logic import *
from src.sat_solver import *

############################## Benchmark Algorithms #########################################
def quine_mccluskey(TruthTables: list[pd.DataFrame]):
    start_time = time.time()
    for table in TruthTables:
        print("quine mccluskey prime implicants", find_prime_implicants(table))
    print(f"quine_mccluskey {time.time() - start_time}, to run")

def paul_elliot(p: Problem, Vs: list[list]):
    start_time = time.time()
    for v in Vs:
        print("elliot prime implicants", find_prime_implicants_elliot(p, v))
    print(f"paul_elliot {time.time() - start_time}, to run")

quine_mccluskey([tableDF_a, tableDF_b, tableDF_c])
paul_elliot(p, [Vs, Vs1, Vs2])