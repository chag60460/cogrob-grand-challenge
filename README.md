# cogrob-grand-challenge

## Paul Elliot Algorithm

- `Benchmark/paul_elliot_algo` contains all the files related to implementing Paul Elliot's prime implicant generation method
    - `elliot.py` contains helper functions used to implement Paul Elliot's algorithm, including validity and satisfiability check
    - `set_up.py` sets up the rocket thruster example, the scenario we use to benchmark the two algorithms
    - `prime_implicants.py` is where Paul Elliot's prime implicant generation algorithm is implemented, using helper functions from `elliot.py`
    

## Quine McCluskey Algorithm

- `Benchmark/quine_mccluskey_algo` contains all the files related to implementing Quine McCluskey prime implicant generation method
    - `utils.py` contains all the help functions and help class that implement Quine McCluskey algorithm,
    - `truth_table_generator.py` sets up the rocket thruster example, then generating xlsx forms from it
    - `quine_mccluskey.py` is where Quine McCluskey prime implicant generation algorithm is implemented

## Benchmark

- `benchmark.py` is where both algorithms are ran and benchmarked
    - `time` is used to keep track of time
    - `tracemalloc` is used to keep track of memory usage
    - the file can be ran using the command `python3 benchmark.py` in terminal

## Other

- `Benchmark/src` contains all the helper classes, such as clauses, assignments, sat solvers, etc.
- `Archive` contains previous iterations, keep track of changes we've made