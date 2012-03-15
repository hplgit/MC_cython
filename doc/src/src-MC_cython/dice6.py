import sys, os, time
import numpy as np
import random

def dice6_py(N, ndice, nsix):
    M = 0                     # no of successful events
    for i in range(N):
        six = 0               # how many dice with six eyes?
        for j in range(ndice):
            r = random.randint(1, 6)  # roll die no. j
            if r == 6:
               six += 1
        if six >= nsix:       # successful event?
            M += 1
    p = float(M)/N
    return p

def dice6_vec1(N, ndice, nsix):
    eyes = np.random.random_integers(1, 6, (N, ndice))
    compare = eyes == 6
    nthrows_with_6 = np.sum(compare, axis=1)  # sum over columns
    nsuccesses = nthrows_with_6 >= nsix
    M = sum(nsuccesses)
    p = float(M)/N
    return p

def dice6_vec2(N, ndice, nsix):
    eyes = np.random.random_integers(1, 6, (N, ndice))
    six = [6 for i in range(ndice)]
    M = 0
    for i in range(N):
        # Check experiment no. i:
        compare = eyes[i,:] == six
        if np.sum(compare) >= nsix:
            M += 1
    p = float(M)/N
    return p


def run_exeriments(N, ndice, nsix):
    try:
        from _dice6_cy import \
             dice61 as dice6_cy1, dice62 as dice6_cy2
        from _dice6_c1 import dice6 as dice6_c_f2py
        from _dice6_c2 import dice6_cwrap as dice6_c_cy
    except ImportError:
        raise ImportError('Extension modules needs to be built. Run make.sh!')

    # Benchmark the various methods
    from scitools.misc import hardware_info
    import pprint; pprint.pprint(hardware_info())
    timings = {}

    t0 = time.clock()
    p = dice6_cy2(N, ndice, nsix)
    t1 = time.clock()
    timings['Cython numpy.random'] = t1-t0
    print '\n\nLoops in Cython with numpy.random: ', t1-t0, p

    t0 = time.clock()
    p = dice6_c_f2py(N, ndice, nsix)
    t1 = time.clock()
    timings['C via f2py'] = t1-t0
    print 'Loops in C, interfaced via f2py        ', t1-t0, p

    t0 = time.clock()
    p = dice6_c_cy(N, ndice, nsix)
    t1 = time.clock()
    timings['C via Cython'] = t1-t0
    print 'Loops in C, interfaced via Cython      ', t1-t0, p

    capp = './dice6.capp'
    if not os.path.isfile(capp):
        raise Exception('stand-alone C program is not compiled!')
    t0 = time.time()
    os.system('time %s %d' % (capp, N))
    t1 = time.time()
    timings['C program'] = t1-t0
    print 'Loops in C, stand-alone C program      %.2f' % (t1-t0)

    t0 = time.clock()
    p = dice6_py(N, ndice, nsix)
    t1 = time.clock()
    timings['Python, plain'] = t1-t0
    print 'Loops in Python:                   ', t1-t0, p

    t0 = time.clock()
    p = dice6_vec1(N, ndice, nsix)
    t1 = time.clock()
    timings['Python, vectorized v1'] = t1-t0
    print 'Vectorized Python v1:              ', t1-t0, p

    t0 = time.clock()
    p = dice6_vec2(N, ndice, nsix)
    t1 = time.clock()
    timings['Python, vectorized v2'] = t1-t0
    print 'Vectorized Python v2:              ', t1-t0, p

    t0 = time.clock()
    p = dice6_cy1(N, ndice, nsix)
    t1 = time.clock()
    timings['Cython random.randint'] = t1-t0
    print 'Loops in Cython with random.randint:', t1-t0, p

    cpu_best = min([timings[m] for m in timings])
    for method in timings:
        print '%s: %.2f' % (method, timings[method]/cpu_best)


    # Profiling of dice6_cy1
    print '\n\n'
    import cProfile, pstats
    cProfile.runctx('dice6_cy1(N, ndice, nsix)', globals(), locals(), '.prof')
    s = pstats.Stats('.prof')
    s.strip_dirs().sort_stats('time').print_stats(30)


    """
    Cython numpy.random: 1.80
    C via f2py: 1.85
    C program: 1.00
    Python, vectorized v1: 24.28
    Python, vectorized v2: 163.75
    Python, plain: 55.20
    C via Cython: 1.78
    Cython random.randint: 47.86


    Old:
    Unix> python dice6.py 300000
    Loops in Python:                    6.06 0.0617433333333
    Vectorized Python v1:               1.54 0.06262
    Vectorized Python v2:               9.72 1.33333333333e-05
    Loops in Cython with random.randint: 5.42 0.0618633333333
    Loops in Cython with numpy.random:  0.07 0.0622866666667
    """

def vary_N_ndice():
    def exact(ndice):
        return 6.0**(-ndice)

    e = [None]*3
    for ndice in 3, 4, 5:
        e.append({})
        for k in 3, 4, 5, 6:
            N = 10**k
            repetitions = 25
            t0 = time.clock()
            e[ndice][N] = [dice6_py(N, ndice, ndice) \
                           for j in range(repetitions)]
            t1 = time.clock()
            cpu = (t1 - t0)/float(repetitions)
            p = e[ndice][N]
            print '%d dice, N=10^%d, mean=%.5f, stdev=%.2e, exact=%.5f, time=%.1f s' % (ndice, k, np.mean(p), np.std(p), exact(ndice), cpu)

if __name__ == '__main__':
    N = int(sys.argv[1])
    ndice = 6
    nsix =3

    #run_experiments(N, ndice, nsix)
    vary_N_ndice()
