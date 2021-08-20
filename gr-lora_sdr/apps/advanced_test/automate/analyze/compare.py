#!/usr/bin/python2
import os, sys, glob
import matplotlib.pyplot as plt
from seri import *

# To be called with ./compare.py task1 task2...


def main(argv):
    # os.chdir("/cortexlab/homes/pesteve/results")
    for dir in argv:
        # os.chdir(os.path.join("/cortexlab/homes/pesteve/results", dir))
        os.chdir(os.path.join("/root", dir))

        paths = glob.glob("res_*.txt")
        l = analyze(paths)
        print("\nNumber of nodes = {}".format(len(l)))
        print("ACK/N = {}".format(ack_rate(l)))
        print("\n")
        
# Tracer M -> sum(ACK)/sum(N) (M)
# Idem mais en separant par SF

if __name__ == '__main__':
    main(sys.argv[1:])