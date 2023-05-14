import time
from paul_elliot_algo.set_up import *
from paul_elliot_algo.prime_implicants import *
from quine_mccluskey_algo.quine_mccluskey import *
from src.propositional_state_logic import *
from src.sat_solver import *

############################## Benchmark Algorithms #########################################
def quine_mccluskey(fileName: str) -> tuple:
    start_time = time.time()
    find_prime_implicants(fileName)
    print(f"quine_mccluskey {time.time() - start_time}, to run")

def paul_elliot(p: Problem, Vs: list[list]):
    start_time = time.time()
    for v in Vs:
        print("elliot prime implicants", find_prime_implicants_elliot(p, v))
    print(f"paul_elliot {time.time() - start_time}, to run")

paul_elliot(p, [Vs, Vs1, Vs2])
#quine_mccluskey('Problem_Theory_v1.xlsx')