#!/usr/bin/python3
import os, sys, glob
# import matplotlib.pyplot as plt
from seri import *

# To be called with ./compare.py task1 task2...


def main(argv):
    # os.chdir("/cortexlab/homes/pesteve/results")
    for dir in argv:
        # os.chdir(os.path.join("/cortexlab/homes/pesteve/results", dir))
        # os.chdir(os.path.join("/root", dir))

        os.chdir(os.path.join("/Users/estevep/Documents/LoRa_PHY_Cxlb/gr-lora_sdr/apps/advanced_test/automate/analyze", dir))
        # os.chdir(os.path.join(".", dir))
        paths = glob.glob("**/res_*.txt", recursive=True)
        l = analyze(paths)
        print("\nNumber of nodes = {}".format(len(l)))
        print("Global ACK/N = {}".format(ack_rate(l)))
        print("--------------------------")
        SFindex = get_SF_index(l)
        for SF in SFindex.keys():
            print("SF = {}".format(SF))
            l_SF = [ l[i] for i in SFindex[SF] ] # List of all the results for this SF
            
            BW_TX_index = get_BW_TX_index(l_SF)
            for BW_TX in BW_TX_index.keys():
                print("\tBW.TX = {}".format(BW_TX))
                l_BW_TX = [ l_SF[i] for i in BW_TX_index[BW_TX] ]
                
                print("\t\t{} nodes".format(len(l_BW_TX)))
                print("\t\tACK/N = {}".format(ack_rate(l_BW_TX)))

def main(argv):
    """
    Objectif: return {N: {SF_nb: {SF:[dict1, dict2]}}}
    """

    fdict = {}

    # os.chdir("/cortexlab/homes/pesteve/results")
    for dir in argv:
        # os.chdir(os.path.join("/cortexlab/homes/pesteve/results", dir))
        # os.chdir(os.path.join("/root", dir))

        os.chdir(os.path.join("/Users/estevep/Documents/LoRa_PHY_Cxlb/gr-lora_sdr/apps/advanced_test/automate/analyze", dir))
        # os.chdir(os.path.join(".", dir))
        paths = glob.glob("**/res_*.txt", recursive=True)
        l = analyze(paths)
        N = len(l)
        print("\nNumber of nodes = {}".format(len(l)))
        print("Global ACK/N = {}".format(ack_rate(l)))
        print("--------------------------")
        SFindex = get_SF_index(l)
        SF_nb = len(SFindex)

        fdict[N]={SF_nb:{}}
        
        for SF in SFindex.keys():
            print("SF = {}".format(SF))

            l_SF = [ l[i] for i in SFindex[SF] ] # List of all the results for this SF
            # Add the results for this SF in the final dictionary
            if len(fdict[N][SF_nb]) == 0:
                fdict[N][SF_nb][SF]=l_SF
            elif len(fdict[N][SF_nb][SF]) == 0:
                fdict[N][SF_nb][SF]=l_SF
            else:
                fdict[N][SF_nb][SF]+=l_SF



            # BW_TX_index = get_BW_TX_index(l_SF)
            # for BW_TX in BW_TX_index.keys():
            #     print("\tBW.TX = {}".format(BW_TX))
            #     l_BW_TX = [ l_SF[i] for i in BW_TX_index[BW_TX] ]
                
            #     print("\t\t{} nodes".format(len(l_BW_TX)))
            #     print("\t\tACK/N = {}".format(ack_rate(l_BW_TX)))

    # {N: {SF_nb: {SF:[dict1, dict2]}}}
    for N, SF_nb_dict in fdict.items():
        print("{} nodes".format(N))
        for SF_nb, SF_dict in SF_nb_dict.items():
            print("\t{} different SF".format(SF_nb))
            for SF, l_SF in SF_dict.items:
                print("\t\tSF={}".SF)
                print("Mean ACK rate: {}".format(ack_rate(l_SF)))
    
    return fdict


                
    # print("\t\t{} nodes".format(len(l_SF)))
    # print("\t\tACK/N = {}".format(ack_rate(l_SF)))
    

Dico:
    {N: {SF_nb:[l1, l2]}}

Dico: {SF:{BW:[]}}
Pour chaque SF:
    Une liste pour chaque BW:


        
        print("\n")
        print("_________________________________________________")
        print("\n")
        
# Tracer M -> sum(ACK)/sum(N) (M)
# Idem mais en separant par SF

if __name__ == '__main__':
    main(sys.argv[1:])
