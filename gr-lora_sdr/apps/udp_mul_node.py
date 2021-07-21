import socket, json, time, argparse

# Idée :
# Pouvoir régler au début : **SF**, CR, GTX, GRX, FTX, FRX, nom du noeud (unique) et la durée de la fenêtre (défaut = 100ms)
# -> plus la fenêtre et courte et avec des SF identiques pour tous les noeuds on devrait avoir plus d'interférences
# Avoir un paramètre binaire (True ou False) pour le caractère aléatoire

# 1 - input de tous les paramètres (à entrer obligatoirement, "" = paramètre par défaut)
# 2 - lancement d'une boucle infinie
#   a - check si le timer est passé en négatif
#       i - si oui alors on remet le timer et on fait un envoi "[NODE NAME]X" où X est le numéro du message
#   b - on écoute
#       i - si message reçu, alors on vérifie qu'il a bien la forme "[NODE NAME]X - ACK" où X est un entier
#           si oui, alors on comptabilise 1 message bien reçu.

# 

TRANSMIT_WINDOW_RATIO = 1/2
RECEIVE_WINDOW_RATIO = 3/4

# t_x = random.random() * TRANSMIT_WINDOW_RATIO * period
# r_x = RECEIVE_WINDOW_RATIO * period
# remaining = period - t_x - r_x
# Node wait for t_x seconds
# Node transmit
# Node receive for RECEIVE_WINDOW_RATIO * period
# Node waits for remaining seconds

# Transmit/Receive cycle of the node: 
#   transmit window -> TRANSMIT_WINDOW_RATIO * period 
#       (transmit at the start of the window if random=False, randomly if True)
#   receive window -> (1-TRANSMIT_WINDOW_RATIO) * period


# Problème :     data, addr = socket_rx.recvfrom(1024) écoute jusqu'à avoir reçu un message -> nécessité de faire 2 tâches

print("LORA Phy layer Python Multiple Node controler - GNU Radio\n")


parser = argparse.ArgumentParser(description="LORA Phy layer Python Multiple Node controler - GNU Radio")
# Upper layer parameters
parser.add_argument('node_id', help="Unique node identifier")
parser.add_argument('--period', type=float, help="Period of the transmitting/receiving cycle in seconds", default=.1)
parser.add_argument('--random', type = bool, default=True)
parser.add_argument('--N', type = int, default=10, help="Number of transmitted message")

# Port numbers
parser.add_argument('--PORT_NO_TX', type = int, default=6788, help="UDP TX port number")
parser.add_argument('--PORT_NO_RX', type = int, default=6790, help="UDP RX port number")


# Physical layer parameters
# parser.add_argument('--SF', type=int, help="Spreading factor")
# parser.add_argument('--CR', type=int, help="Coding Rate")
# parser.add_argument('--CRC', type = bool, default=True)
# parser.add_argument('--GTX', type = float, default=30, help="Gain for TX chain")
# parser.add_argument('--GRX', type = float, default=20, help="Gain for RX chain")
parser.add_argument('--FTX', type = float, default=910e6, help="USRP frequency for TX chain")
parser.add_argument('--FRX', type = float, default=900e6, help="USRP frequency for RX chain")


# dyn_parameters = {  "CR" : "Coding Rate", 
#                     "SF" : "Spreading Factor",
#                     "GTX": "Gain for TX chain", 
#                     "GRX": "Gain for RX chain",
#                     "FTX": "USRP frequency for TX chain",
#                     "FRX": "USRP frequency for RX chain",
#                     "MSG": "Data to transmit",
#                     "print" : "Print in GNURADIO current parameters"
#                 } 

args = parser.parse_args()
cmd_dict = vars(args)

PORT_NO_TX = cmd_dict.pop('PORT_NO_TX')
PORT_NO_RX = cmd_dict.pop('PORT_NO_RX')
IP_ADDRESS = "127.0.0.1"


upper_param_key = ["node_id", "period", "random", "N"]
upper_param = {}
for key in upper_param_key:
    upper_param[key] = cmd_dict.pop(key)

period = upper_param.get("period")

# Parameters recap
print('Upper layer parameters:')
for key in upper_param.keys():
    print("{}= {}".format(key, upper_param[key]))

print("\nPhysical layer parameters:")

for key in cmd_dict.keys():
    print("{}= {}".format(key, cmd_dict[key]))


# cmd_dict = {}

# Init PHY layer in GNU Radio
# cmd_dict = {    #"CR" : "4", 
#                 #"SF" : "8",
#                 #"GTX": "60", 
#                 #"GRX": "60",
#                 "FTX": "910e6",
#                 "FRX": "900e6"
#             } 


socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
socket_tx.close()
cmd_dict.clear()


print("\n")

# transmit_timing = random.random() * TRANSMIT_WINDOW_RATIO * period
# rx_duration = RECEIVE_WINDOW_RATIO * period
# t_left = period - transmit_timing - rx_elapsed_time
# Node transmit
# Node listens for rx_duration or until it receives a valid acknowledgement
# Node waits for t_left seconds 

# Transmit/Receive cycle of the node: 
#   transmit window -> TRANSMIT_WINDOW_RATIO * period 
#       (transmit at the start of the window if random=False, randomly if True)
#   receive window -> (1-TRANSMIT_WINDOW_RATIO) * period

rx_duration = RECEIVE_WINDOW_RATIO * period
rx_counter = 0

for i in range(upper_param["N"]):
    # Node waits for transmit_timing seconds (0 if random is set to false)
    transmit_timing = random.random() * TRANSMIT_WINDOW_RATIO * period * int(upper_param["random"])
    time.sleep(transmit_timing)

    # Node transmits
    cmd_dict = {"MSG":"Packet {} from node {}".format(i, upper_param["node_id"])}
    socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
    socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
    socket_tx.close()

    # Node listens for rx_duration
    socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_rx.bind((IP_ADDRESS, PORT_NO_RX))
    
    received_msg = {"msg":""}

    elapsed = 0
    start = time.perf_counter()
    
    while received_msg["msg"] != "ACK-Packet {} from node {}".format(i, upper_param["node_id"])\
            and elapsed < rx_duration:
        ready = select.select([socket_rx],[],[],rx_duration - elapsed)
        if ready[0]:
            data, addr = socket_rx.recvfrom(1024)
            received_msg = json.loads("".join([chr(item) for item in data]))
        elapsed = time.perf_counter() - start

    # If a valid acknowledgement was received, increase the rx_counter
    if received_msg["msg"] == "ACK-Packet {} from node {}".format(i, upper_param["node_id"]):
        rx_counter += 1

    time.sleep(period - transmit_timing - elapsed)
    
print("{}/{} acknowledgements received".format(rx_counter,upper_param["N"]))



        
        

        
    





while(True):
    cmd = str(input("Enter the parameter OR \"send\" to send all stored commands :"))
    if cmd == "send":
        if len(cmd_dict) != 0:
            socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
            
            socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
            start = time.perf_counter()
            socket_tx.close()
            cmd_dict.clear()

            print("Command send to LORA physical layer in GNURADIO -------> Waiting for transmission\n")


            # socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # socket_rx.bind((IP_ADDRESS, PORT_NO_RX))
            # received = False
            
            # while not received:
            #     data, addr = socket_rx.recvfrom(1024)
            #     end = time.perf_counter()
            #     received_msg = json.loads("".join([chr(item) for item in data]))
            #     print ("Message transmited !")
            #     for key in received_msg.keys():
            #         print("     " + key + " : " + received_msg[key])
            #     print ("Elapsed time : " + str(end - start) + " [scd]")
            #     print("\n")
            #     received = True


        else:
            print("Your command list is empty\n")

    elif cmd in dyn_parameters.keys(): 
        # Add verification of the param type (int/float/etc)
        param_value = str(input("Enter the new value of the " + dyn_parameters[cmd] + " :"))
        cmd_dict.update({cmd:param_value})
        print("Command added to list : " + str(cmd_dict) + "\n")

    else:
        print("Unknown command, please try again\n")

