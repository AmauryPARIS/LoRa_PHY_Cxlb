import socket, json, time, argparse, random, select

TRANSMIT_WINDOW_RATIO = 2/5
RECEIVE_WINDOW_RATIO = 2/5

# Transmit/Receive cycle of the node: 
#   transmit window -> TRANSMIT_WINDOW_RATIO * period 
#       (transmit at the start of the window if random=False, randomly in TX window if True)
#   receive window -> RECEIVE_WINDOW_RATIO * period

print("LORA Phy layer Python Multiple Node controler - GNU Radio\n")


parser = argparse.ArgumentParser(description="LORA Phy layer Python Multiple Node controler - GNU Radio")

# Upper layer parameters
parser.add_argument('node_id', help="Unique node identifier")
parser.add_argument('--period', type=float, \
    help="Period of the transmitting/receiving cycle in seconds", default=1.5)
parser.add_argument('--random', type = bool, default=True, \
    help="True = Transmit at a random timing in TX window, False = transmit at the beginning of the TX window")
parser.add_argument('--N', type = int, default=10, help="Number of transmitted message")

# Port numbers
parser.add_argument('--PORT_NO_TX', type = int, default=6788, help="UDP TX port number")
parser.add_argument('--PORT_NO_RX', type = int, default=6790, help="UDP RX port number")


# Physical layer parameters - to be tested
parser.add_argument('--SF.TX', type=int, help="Spreading factor", default=7)
parser.add_argument('--CR.TX', type=int, help="Coding Rate", default=4)
# parser.add_argument('--CRC.TX', type = int, default=1, help="CRC presence, 1 = True, 0 = False")
parser.add_argument('--G.TX', type = float, default=30, help="Gain for TX chain")
parser.add_argument('--G.RX', type = float, default=20, help="Gain for RX chain")
# parser.add_argument('--F.TX', type = float, default=910e6, help="USRP frequency for TX chain")
# parser.add_argument('--F.RX', type = float, default=900e6, help="USRP frequency for RX chain")
# parser.add_argument('--BW.TX', type = float, default=250e3, help="Bandwidth for TX chain")
# parser.add_argument('--BW.RX', type = float, default=900e6, help="Bandwidth for RX chain")

# dyn_parameters = {  "CR.TX" : "Coding Rate", 
#                     "SF.TX" : "Spreading Factor",
#                     "G.TX": "Gain for TX chain", 
#                     "G.RX": "Gain for RX chain",
#                     "F.TX": "USRP frequency for TX chain",
#                     "F.RX": "USRP frequency for RX chain",
#                     "MSG": "Data to transmit",
#                     "print" : "Print in GNURADIO current parameters"
#                 } 

# Parsing
args = parser.parse_args()
cmd_dict = vars(args)

PORT_NO_TX = cmd_dict.pop('PORT_NO_TX')
PORT_NO_RX = cmd_dict.pop('PORT_NO_RX')
IP_ADDRESS = "127.0.0.1"

# Upper layer parameters
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

# Init PHY layer in GNU Radio

# cmd_dict = {    #"CR.TX" : "4", 
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

rx_duration = RECEIVE_WINDOW_RATIO * period
rx_counter = 0

socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_rx.bind((IP_ADDRESS, PORT_NO_RX))

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

    # Node listens for rx_duration or until it receives a valid acknowledgement
    
    received_msg = {"msg":""}

    elapsed = 0
    start = time.perf_counter()
    
    while received_msg["msg"] != "ACK-Packet {} from node {}".format(i, upper_param["node_id"])\
            and elapsed < rx_duration:
        ready = select.select([socket_rx],[],[],rx_duration - elapsed)
        if ready[0]:
            data, addr = socket_rx.recvfrom(1024)
            received_msg = json.loads("".join([chr(item) for item in data]))
            # print("DEBUG: Received message: {}".format(received_msg["msg"]))
            # print("DEBUG: Expected message: ACK-Packet {} from node {}\n".format(i, upper_param["node_id"]))
        elapsed = time.perf_counter() - start

    # If a valid acknowledgement was received, increase the rx_counter
    if received_msg["msg"] == "ACK-Packet {} from node {}".format(i, upper_param["node_id"]):
        rx_counter += 1
    else:
        print("No ACK received on message {}".format(i))

    # print(f"DEBUG: Period = {period}s")
    # print(f"DEBUG: Total elapsed time = {transmit_timing + elapsed}s\n")
    if (period - transmit_timing - elapsed > 0):
        # Node waits for the end of the period
        time.sleep(period - transmit_timing - elapsed)
        
        
    
print("{}/{} = {}% acknowledgements received".format(rx_counter,upper_param["N"],100*rx_counter/upper_param["N"]))


