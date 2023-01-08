def cube(x):
    return x**3




if __name__ == "__main__":
    from multiprocessing.dummy import Pool #<- multiprocessing.dummy to set up a pool of threads -> same pid

    pool = Pool(processes=4)

    results = pool.map(cube, range(1,7))

    print(results)