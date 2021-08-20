#!/usr/bin/python2
import os, sys
import matplotlib.pyplot as plt

# to be called with ./analyze.py `find /root -name res_*.txt`

def analyze(paths):
    """
    Returns a list of dictionaries, containing all parameters (SF, BW...) \
    and results (number of transmitted message, number of acknoledgments received) of each node
    """
    M = len(paths) # number of nodes
    print("Results found: {}".format(paths))
    print("Number of result files: {}".format(M))

    l = [{} for i in range(M)]

    param = [
        "node_id",
        "N",
        "ACK",
        "period",
        "rand",
        "SF",
        "BW.TX",
        "BW.RX",
        "F.TX",
        "F.RX",
        "G.TX",
        "G.RX"
        ]
    
    param_type = {
        "node_id" : str,
        "N" : int,
        "ACK" : int,
        "period" : float,
        "rand" : bool,
        "SF" : int,
        "BW.TX" : float,
        "BW.RX" : float,
        "F.TX" : float,
        "F.RX" : float,
        "G.TX" : float,
        "G.RX" : float
    }

    for i in range(M):
        path = paths[i]

        with open(path) as f:
            line_counter = 0
            for line in f:
                if not line.startswith("#"):
                    # print(line)
                    try:
                        cur_param = param[line_counter]
                        l[i][cur_param] = param_type[cur_param](line) # Try conversion
                        line_counter += 1
                    except ValueError:
                        print("Error while analyzing the result file {}: invalid {}"\
                            .format(path, param[line_counter]))
                        break

    return l

def ack_rate(l):
    M = len(l)
    Ntot = sum((l[i]["N"] for i in range(M)))
    ACKtot = sum((l[i]["ACK"] for i in range(M)))
    rate = Ntot/ACKtot
    return rate

def main(argv):
    print("ACK/N = {}".format(ack_rate(analyze(argv))))
        
# Tracer M -> sum(ACK)/sum(N) (M)
# Idem mais en separant par SF

if __name__ == '__main__':
    main(sys.argv[1:])