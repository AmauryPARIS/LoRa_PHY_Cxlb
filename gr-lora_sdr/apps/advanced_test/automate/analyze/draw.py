#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# import compare
import glob
import numpy as np
from seri import *

def plot_diff_node_nb(argv):
    """
    Plots the graph of the mean acknoledgment rate for different numbers of nodes
    """
    # os.chdir("/cortexlab/homes/pesteve/results")
    k = 0
    l_N=[]
    l_ack_rate=[]
    for dir in argv:
        # For each task :
        
        # os.chdir(os.path.join("/cortexlab/homes/pesteve/results", dir))
        # os.chdir(os.path.join("/root", dir))

        os.chdir(os.path.join("/Users/estevep/Documents/LoRa_PHY_Cxlb/gr-lora_sdr/apps/advanced_test/automate/analyze", dir))
        paths = glob.glob("**/res_*.txt", recursive=True)
        l = analyze(paths)
        if len(l)==0:
            print("No result found")
            continue 
        print("\nNumber of nodes = {}".format(len(l)))
        print(f"{l=}")
        l_ack_rate.append(ack_rate(l))
        l_N.append(len(l))
        print("Global ACK/N = {}".format(l_ack_rate[k]))
        print("--------------------------")
        # SFindex = get_SF_index(l)
        # for SF in SFindex.keys():
        #     print("SF = {}".format(SF))
        #     l_SF = [ l[i] for i in SFindex[SF] ] # List of all the results for this SF
            
        #     BW_TX_index = get_BW_TX_index(l_SF)
        #     for BW_TX in BW_TX_index.keys():
        #         print("\tBW.TX = {}".format(BW_TX))
        #         l_BW_TX = [ l_SF[i] for i in BW_TX_index[BW_TX] ]
                
        #         print("\t\tACK/N = {}".format(ack_rate(l_BW_TX)))
        
        print("\n")
        print("_________________________________________________")
        print("\n")

        k+=1

    # print(f"{l_N=}")
    # print(f"{l_ack_rate=}")
    
    indexes = np.argsort(np.array(l_N))
    l_N.sort()
    l_ack_rate = [l_ack_rate[i] for i in indexes]

    print(l_ack_rate)
    
    # print(f"{l_N=}")
    # print(f"{l_ack_rate=}")
    
    plt.figure()
    plt.scatter(l_N, l_ack_rate, marker='+')
    plt.xlabel("Number of nodes")
    plt.ylabel("Acknoledgment rate (100 messages/node)")
    plt.title("Acknoledgment rate variations for different node numbers (up to 6 nodes)")
    plt.show()


def plot_diff_SF_nb(argv):
    """
    Plots the graph of the mean acknoledgment rate for different numbers of SF
    """
    # os.chdir("/cortexlab/homes/pesteve/results")
    l_SF_nb=[]
    l_ack_rate=[]
    k=0
    for dir in argv:
        # os.chdir(os.path.join("/cortexlab/homes/pesteve/results", dir))
        # os.chdir(os.path.join("/root", dir))

        os.chdir(os.path.join("/Users/estevep/Documents/LoRa_PHY_Cxlb/gr-lora_sdr/apps/advanced_test/automate/analyze", dir))
        paths = glob.glob("**/res_*.txt", recursive=True)
        l = analyze(paths)
        if len(l)==0:
            print("No result found")
            continue 
        print("\nNumber of nodes = {}".format(len(l)))
        l_ack_rate.append(ack_rate(l))
        print(f"{l=}")
        print(f"Before adding: {l_SF_nb=}")
        # l_SF_nb.append(l[0]["SF"] )# Only works when all nodes have the same SF
    
        l_SF_nb.append(len({l[i]["SF"] for i in range(len(l))}))
        print(f"After adding: {l_SF_nb=}")
        print("Global ACK/N = {}".format(l_ack_rate[k]))
        k+=1

    # print(f"{l_SF_nb=}")
    # print(f"{l_ack_rate=}")
    
    # Sort the lists before ploting the graph
    indexes = np.argsort(np.array(l_SF_nb))
    l_SF_nb.sort()
    l_ack_rate = [l_ack_rate[i] for i in indexes]
    
    # print(f"{l_SF_nb=}")
    # print(f"{l_ack_rate=}")


    plt.figure()
    plt.scatter(l_SF_nb, l_ack_rate, marker='+')
    plt.xlabel("Number of SF")
    plt.ylabel("Acknoledgment rate (500 messages/node)")
    plt.title("Acknoledgment rate variations for different SF numbers (6 nodes)")
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.1))
    plt.gca().xaxis.set_major_locator(MultipleLocator(1))

    plt.show()


def main(argv):
    # plot_diff_node_nb(argv)
    plot_diff_SF_nb(argv)

if __name__ == '__main__':
    main(sys.argv[1:])


# def main(argv):
#     # os.chdir("/cortexlab/homes/pesteve/results")
#     for dir in argv:
#         os.chdir(os.path.join("/cortexlab/homes/pesteve/results", dir))
#         # os.chdir(os.path.join("/root", dir))

#         paths = glob.glob("**/res_*.txt", recursive=True)
#         l = analyze(paths)
#         print("\nNumber of nodes = {}".format(len(l)))
#         print("Global ACK/N = {}".format(ack_rate(l)))
#         print("--------------------------")
#         SFindex = get_SF_index(l)
#         for SF in SFindex.keys():
#             print("SF = {}".format(SF))
#             l_SF = [ l[i] for i in SFindex[SF] ] # List of all the results for this SF
            
#             BW_TX_index = get_BW_TX_index(l_SF)
#             for BW_TX in BW_TX_index.keys():
#                 print("\tBW.TX = {}".format(BW_TX))
#                 l_BW_TX = [ l_SF[i] for i in BW_TX_index[BW_TX] ]
                
#                 print("\t\tACK/N = {}".format(ack_rate(l_BW_TX)))

        
#         print("\n")
#         print("_________________________________________________")
#         print("\n")
