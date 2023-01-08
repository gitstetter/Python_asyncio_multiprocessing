import random
import time
import os

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

    from multiprocessing.dummy import Pool #<- multiprocessing.dummy to set up a pool of threads -> same pid


    nbr_samples_in_total = 1e9
    nbr_parallel_blocks = 4
    pool = Pool(processes=nbr_parallel_blocks)
    nbr_samples_per_worker = nbr_samples_in_total / nbr_parallel_blocks
    print("Making {:,} samples per {} worker threads".format(nbr_samples_per_worker, nbr_parallel_blocks))
    nbr_trials_per_process = [nbr_samples_per_worker] * nbr_parallel_blocks
    t1 = time.time()
    nbr_in_quarter_unit_circles = pool.map(estimate_nbr_points_in_quarter_circle, nbr_trials_per_process)
    pi_estimate = sum(nbr_in_quarter_unit_circles) * 4 / float(nbr_samples_in_total)
    print("Estimated pi", pi_estimate)
    print("Delta:", time.time() - t1)

# Making 250,000,000.0 samples per 4 worker threads
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000.0 on pid 30580
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000.0 on pid 30580
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000.0 on pid 30580
# Executing estimate_nbr_points_in_quarter_circle with 250,000,000.0 on pid 30580
# Estimated pi 3.141628796
# Delta: 578.0471358299255 -> ±4x duration compared to individual processes