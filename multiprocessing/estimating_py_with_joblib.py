import random
import os
import time
from joblib import Parallel, delayed

def estimate_nbr_points_in_quarter_circle(nbr_estimates):
    """Monte carlo estimate of the number of points in a quarter circle using pure Python"""
    print(f"Executing estimate_nbr_points_in_quarter_circle with {nbr_estimates:,} on pid {os.getpid()}")
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
        (delayed(estimate_nbr_points_in_quarter_circle)\
        
        (nbr_samples_per_worker) for sample_idx in range(nbr_parallel_blocks))

    pi_estimate = sum(nbr_in_quarter_unit_circles) * 4 / float(nbr_samples_in_total)
    print("Estimated pi", pi_estimate)
    print("Delta:", time.time() - t1)

# Making 250,000,000 samples per 4 worker
# [Parallel(n_jobs=4)]: Using backend LokyBackend with 4 concurrent workers.
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 on pid 8613
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 on pid 8614
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 on pid 8616
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000 on pid 8615
# [Parallel(n_jobs=4)]: Done   2 out of   4 | elapsed:  2.9min remaining:  2.9min
# [Parallel(n_jobs=4)]: Done   4 out of   4 | elapsed:  2.9min finished
# Estimated pi 3.141592472
# Delta: 176.76421999931335 +20 seconds compared to multiple processes