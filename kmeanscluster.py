# Input: number of iterations L
#        number of clusters k
#        numpy matrix X of features, with n rows (samples), d columns (features)   
#
# Output: numpy vector a of n rows, 1 column
#            a[i] is the cluster assignment for the i-th sample (an integer from 0 to k-1)
#        number of iterations that were actually executed (iter+1)
import numpy as np
import numpy.linalg as la
def run(L,k,X):
    n, d = X.shape
    a = np.zeros((n,1))
    r = np.zeros((k,d))
    q = np.random.choice(n,k,replace=False)
    for j in range(k):
        r[j] = X[q[j]]
    for iter in range(L):
        at_least_one_change = False
        for t in range(0,n):
            c = 0
            b = la.norm(X[t]-r[0])
            for j in range(1,k):
                if (la.norm(X[t]-r[j])) < b:
                    c = j
                    b = la.norm(X[t]-r[j])
            if a[t][0] != c:
                a[t][0] = c
                at_least_one_change = True
        if not at_least_one_change:
            break
        for j in range(k):
            s = np.zeros(d)
            m = 0
            for t in range(n):
                if a[t][0]==j:
                    s = s + X[t]
                    m = m + 1
            r[j] = s/m
    return a, iter+1