# first line: 8
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
