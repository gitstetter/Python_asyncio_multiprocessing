import random
import os
import time
from joblib import Parallel, delayed, Memory

memory = Memory("./joblib_cache", verbose=0)

@memory.cache
def estimate_nbr_points_in_quarter_circle_with_idx(nbr_estimates, idx):
    """Monte carlo estimate of the number of points in a quarter circle using pure Python.
    Includes idx to make calls for caching unique"""
    print(f"Executing estimate_nbr_points_in_quarter_circle with {nbr_estimates:,} for idx {idx} on pid {os.getpid()}")
    nbr_trials_in_quarter_unit_circle = 0
    for step in range(int(nbr_estimates)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_quarter_unit_circle += is_in_unit_circle

    return nbr_trials_in_quarter_unit_circle


if __name__ == "__main__":
    nbr_samples_in_total = int(1e9)
    nbr_parallel_blocks = 4

    nbr_samples_per_worker = int(nbr_samples_in_total / nbr_parallel_blocks)
    print("Making {:,} samples per {} worker".format(nbr_samples_per_worker, nbr_parallel_blocks))
    t1 = time.time()
    nbr_in_quarter_unit_circles = Parallel(n_jobs=nbr_parallel_blocks, verbose=1)\
        (delayed(estimate_nbr_points_in_quarter_circle_with_idx)\
        
        (nbr_samples_per_worker, sample_idx) for sample_idx in range(nbr_parallel_blocks))

    pi_estimate = sum(nbr_in_quarter_unit_circles) * 4 / float(nbr_samples_in_total)
    print("Estimated pi", pi_estimate)
    print("Delta:", time.time() - t1)

###Second run###
# Making 250,000,000 samples per 4 worker
# [Parallel(n_jobs=4)]: Using backend LokyBackend with 4 concurrent workers.
# [Parallel(n_jobs=4)]: Done   2 out of   4 | elapsed:    3.6s remaining:    3.6s
# [Parallel(n_jobs=4)]: Done   4 out of   4 | elapsed:    3.6s finished
# Estimated pi 3.141632764
# Delta: 3.5874979496002197 <------

###First Run###
# Making 250,000,000 samples per 4 worker
# [Parallel(n_jobs=4)]: Using backend LokyBackend with 4 concurrent workers.
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 for idx 0 on pid 10280
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 for idx 1 on pid 10281
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 for idx 2 on pid 10282
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 for idx 3 on pid 10283
# [Parallel(n_jobs=4)]: Done   2 out of   4 | elapsed:  2.7min remaining:  2.7min
# [Parallel(n_jobs=4)]: Done   4 out of   4 | elapsed:  2.8min finished
# Estimated pi 3.141632764
# Delta: 167.08158087730408 <-----
