#/usr/bin/python2
import os, sys
# import matplotlib.pyplot as plt

# to be called with ./seri.py `find /cortexlab/homes/[username]/results/task_[task_number] -name res_*.txt`

def analyze(paths):
    """
    Returns a list of dictionaries, containing all parameters (SF, BW...) \
    and results (number of transmitted message, number of acknoledgments received) of each node
    """
    M = len(paths) # number of nodes
    if __name__ == '__main__':
        print("Results found: {}".format(paths))
        print("Number of result files (nodes): {}".format(M))

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
    """
    Returns the mean acknoledgment rate for all the nodes in l
    """
    M = len(l)
    if M == 0:
        print("No result in given list")
        return 0
    Ntot = sum((l[i]["N"] for i in range(M)))
    ACKtot = sum((l[i]["ACK"] for i in range(M)))
    rate = float(ACKtot)/Ntot
    return rate

def get_SF_index(l):
    """
    Returns a dictionnary with the following structure:
    {SF:[i, j, ...]} where the integers in the list are the indexes of l such as l[i]["SF"]=SF
    """
    M = len(l)
    if M == 0:
        print("No result in given list")
        return {}
    dict = {}
    for i in range(M):
        if l[i]["SF"] in dict:
            dict[l[i]["SF"]].append(i)
        else:
            dict[l[i]["SF"]] = [i]
    return dict

def get_BW_TX_index(l):
    """
    Returns a dictionnary with the following structure:
    {BW_TX:[i, j, ...]} where the integers in the list are the indexes of l such as l[i]["BW.TX"]=BW_TX
    """
    M = len(l)
    if M == 0:
        print("No result in given list")
        return 0
    dict={}
    for i in range(M):
        if l[i]["BW.TX"] in dict:
            dict[l[i]["BW.TX"]].append(i)
        else:
            dict[l[i]["BW.TX"]] = [i]
    return dict

def main(argv):
    print("ACK/N = {}".format(ack_rate(analyze(argv))))
        
# Tracer M -> sum(ACK)/sum(N) (M)
# Idem mais en separant par SF

if __name__ == '__main__':
    main(sys.argv[1:])
