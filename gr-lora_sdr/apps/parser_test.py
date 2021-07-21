import argparse, sys

# gtx = input("GTX? ")
# grx = input("GRX? ")
# ftx = input("FTX? ")
# frx = input("FRX? ")
# node_id = input("Unique Node ID? ")

# period = input("Window period [100 ms]? ")
# if period == "":
#     period_f = .1
# try:
#     period_f = float(period)
# except ValueError:
#     print("Period value (in s) must be a float")
#     print("Using the default 100ms period\n")

# rd = input("Random transmit timing?")
# try:
#     rd_b = bool(newvalue)
# except ValueError:
#     print("Must be a boolean")
#     print("Defaulting to True")
#     rd_b = True

parser = argparse.ArgumentParser(description="LORA Phy layer Python Multiple Node controler - GNU Radio")
# Upper layer parameters
parser.add_argument('node_id', help="Unique node identifier")
parser.add_argument('--period', type=float, help="Period of the transmitting/receiving cycle in seconds", default=.1)
parser.add_argument('--random', type = bool, default=True)

# Physical layer parameters
parser.add_argument('--SF', action='store', type=int, help="Spreading factor")
parser.add_argument('--CRC', type = bool, default=True)
parser.add_argument('--GTX', type = float, default=30)
parser.add_argument('--GRX', type = float, default=20)
parser.add_argument('--FTX', type = float, default=910e6)
parser.add_argument('--FRX', type = float, default=900e6)

args = parser.parse_args()
arg_dict = vars(args)

upper_param_key = ["node_id", "period", "random"]
upper_param = {}
for key in upper_param_key:
    upper_param[key] = arg_dict.pop(key)

print('Upper layer parameters:')
for key in upper_param.keys():
    print("{}= {}".format(key, upper_param[key]))

print("\nPhysical layer parameters:")

for key in arg_dict.keys():
    print("{}= {}".format(key, arg_dict[key]))

if (arg_dict["CRC"]):
    print("CRC on, {} commands".format(len(arg_dict)))
# print("Nombre d'arguments: {}", format(args.len()))
# sf = args.sf
# crc = args.CRC

# print("CRC: {}; SF: {}", format(sf, crc))



#################################
## Old version
################################
# Initialization
# sf = input("SF? ")
# cr = input("CR? ")
# gtx = input("GTX? ")
# grx = input("GRX? ")
# ftx = input("FTX? ")
# frx = input("FRX? ")
# node_id = input("Unique Node ID? ")

# period = input("Window period [100 ms]? ")
# if period == "":
#     period_f = .1
# try:
#     period_f = float(period)
# except ValueError:
#     print("Period value (in s) must be a float")
#     print("Using the default 100ms period\n")

# rd = input("Random transmit timing?")
# try:
#     rd_b = bool(newvalue)
# except ValueError:
#     print("Must be a boolean")
#     print("Defaulting to True")
#     rd_b = True
    

# # **SF**, CR, GTX, GRX, FTX, FRX, nom du noeud (unique) et la durée de la fenêtre (défaut = 100ms)

# cmd_dict.update({"SF":sf})
# cmd_dict.update({"CR":cr})
# cmd_dict.update({"GTX":gtx})
# cmd_dict.update({"GRX":grx})
# cmd_dict.update({"FTX":ftx})
# cmd_dict.update({"FRX":frx})