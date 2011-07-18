#!/usr/bin/python2
import sys
import os
from density_matrix import System
import numpy as np
import pickle #pickle is not very safe

def plot(n):
    """
    Plot using gnuplot. 
    """
    f=open('./tmp.gp','w')
    f.write('set terminal png\nset output \'graph.png\'\n')
    tmp_str = 'plot \'%s\' using 1:2 with lines'%file_out
    for i in range(n-1):
        tmp_str += ', \'%s\' using 1:%d with lines'%(file_out,i+3)
    tmp_str += '\n'
    f.write(tmp_str)
    f.close()
    os.system('gnuplot tmp.gp')
    os.remove('tmp.gp')

if __name__ ==  '__main__':
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    
    # dictf = open('three_level','w')
    # pickle.dump(parameter,dictf)
    # dictf.close()

    dictf = open(file_in,'r')
    parameter = eval(dictf.read())
#    parameter = pickle.load(dictf)
    dictf.close()
    
    # txtf = open(file_in+'.txt','w')
    # txtf.write(str(parameter))
    # txtf.close()

    system = System(parameter)
    parameter['sweep_profile'].append(file_out)
    system.sweep(*parameter['sweep_profile'])# can parameter add after unpack array?
    plot(parameter['n'])
