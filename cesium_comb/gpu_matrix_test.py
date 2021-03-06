#!/usr/bin/python2
from gpu_matrix import GPU_Matrix
import numpy as np
import time 
MATRIX_SIZE = 2048
gpu = GPU_Matrix(MATRIX_SIZE)
a = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float64)
b = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float64)
c = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float64)
d = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float64)
f = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float64)
g = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float64)
A = a+b*1j
B = c+d*1j

t = time.time()
gpu.matrix_mul(a,b,c,d,f,g)
result_g = f+g*1j
print 'gpu time: ', time.time() - t
t = time.time()
result_c = np.dot(A,B)
print 'cpu time: ',time.time() - t

print result_c
print result_g
print np.linalg.norm(result_c- result_g)
