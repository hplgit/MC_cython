# cython: profile=True
import random

def dice61(int N, int ndice, int nsix):
    cdef int M = 0            # no of successful events
    cdef int six, r
    cdef double p
    for i in range(N):
        six = 0               # how many dice with six eyes?
        for j in range(ndice):
            # Roll die no. j
            r = random.randint(1, 6)
            if r == 6:
               six += 1
        if six >= nsix:       # successful event?
            M += 1
    p = float(M)/N
    return p

import  numpy as np
cimport numpy as np
import cython
@cython.boundscheck(False)
def dice62(int N, int ndice, int nsix):
    # Use numpy to generate all random numbers
    cdef int M = 0            # no of successful events
    cdef int six, r
    cdef double p
    cdef np.ndarray[np.int_t,
                    ndim=2,
                    negative_indices=False,
                    mode='c'] eyes = \
                    np.random.random_integers(1, 6, (N, ndice))
    for i in range(N):
        six = 0               # how many dice with six eyes?
        for j in range(ndice):
            r = eyes[i,j]     # roll die no. j
            if r == 6:
               six += 1
        if six >= nsix:       # successful event?
            M += 1
    p = float(M)/N
    return p


