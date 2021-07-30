import socket, json, time, argparse, random, select

RECEIVE_WINDOW_RATIO = 1

# Transmit/Receive cycle of the node: 
#   transmit window -> TRANSMIT_WINDOW_RATIO * period 
#       (transmit at the start of the window if random=False, randomly in TX window if True)
#   receive window -> RECEIVE_WINDOW_RATIO * period

print("LORA Phy layer Python Node controler to test all TX parameters dynamism - GNU Radio\n")

parser = argparse.ArgumentParser(description="LORA Phy layer Python Node controler to test all TX parameters dynamism - GNU Radio")

# Upper layer parameters
parser.add_argument('node_id', help="Unique node identifier")
parser.add_argument('--period', type=float, \
    help="Period of the transmitting/receiving cycle in seconds", default=.75)

N = 44


# Port numbers
parser.add_argument('--PORT_NO_TX', type = int, default=6788, help="UDP TX port number")
parser.add_argument('--PORT_NO_RX', type = int, default=6790, help="UDP RX port number")


# Parsing
args = parser.parse_args()
cmd_dict = vars(args)

PORT_NO_TX = cmd_dict.pop('PORT_NO_TX')
PORT_NO_RX = cmd_dict.pop('PORT_NO_RX')
IP_ADDRESS = "127.0.0.1"

# Upper layer parameters
upper_param_key = ["node_id", "period"]
upper_param = {}
for key in upper_param_key:
    upper_param[key] = cmd_dict.pop(key)

period = upper_param.get("period")

# Parameters recap
print('Upper layer parameters:')
for key in upper_param.keys():
    print("{}= {}".format(key, upper_param[key]))



# Init PHY layer in GNU Radio

cmd_dict = {    "CR.TX" : "4", 
                "SF.TX" : "7",
                "CRC.TX" : "1",
                "G.TX": "30", 
                "G.RX": "30",
                "F.TX": "900e6",
                "F.RX": "910e6",
                "BW.TX": "250e3",
            } 

print("\nPhysical layer parameters:")

for key in cmd_dict.keys():
    print("{}= {}".format(key, cmd_dict[key]))

print("\n")

rx_duration = RECEIVE_WINDOW_RATIO * period
rx_counter = 0 # number of received acknowledgements
acks = [] # list of received acknowledgements
crc_diff = []
cr_diff = []

socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_rx.bind((IP_ADDRESS, PORT_NO_RX))

for i in range(N):

    # Node transmits
    cmd_dict["MSG"] = "Packet {} from node {}".format(i, upper_param["node_id"])
    if i == 0: 
        cmd_dict["CR.TX"] = "3"
    elif i == 4: 
        cmd_dict["CR.TX"] = "4"
        cmd_dict["SF.TX"] = "8"
    elif i == 8: 
        cmd_dict["SF.TX"] = "7"
    elif i == 12:
        cmd_dict["BW.TX"] = "500e3"
    elif i == 16: 
        cmd_dict["BW.TX"] = "250e3"
    elif i == 20: 
        cmd_dict["F.TX"] = "800e6"
    elif i == 24: 
        cmd_dict["F.TX"] = "900e6"
    elif i == 28:
        cmd_dict["F.RX"] = "800e6"
    elif i == 32:
        cmd_dict["F.RX"] = "910e6"
    elif i == 36:
        cmd_dict["CRC.TX"] = "0"
    elif i == 40:
        cmd_dict["CRC.TX"] = "1"

    print("\nPhysical layer parameters:")

    for key in cmd_dict.keys():
        print("{}= {}".format(key, cmd_dict[key]))
    
    
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

        # Performance indicators
        acks += [i]
        if cmd_dict["CRC.TX"] == "1":
            if received_msg["crc_valid"] != "True":
                crc_diff += [i]
        else:
            if received_msg["crc_valid"] == "True":
                crc_diff += [i]
        if cmd_dict["CR.TX"] != received_msg["CR"]:
            cr_diff += [i]

        

    else:
        print("No ACK received on message {}".format(i))

###########################        

print("\n")

## Results

# Acknowledgements
ack_expected = [i for i in range(0, 4)] + [i for i in range(8,12)] \
    + [i for i in range(16, 20)] + [i for i in range(24,28)] + [i for i in range(32,44)]

missing_acks = list(set(ack_expected) - set(acks))

if len(missing_acks) > 0:
    print ("Missing acknowledgements:\n{}".format(missing_acks))
else:
    print("No missing acknowledgement")

additional_acks = list(set(acks) - set(ack_expected))
if len(additional_acks) > 0:
    print ("Acknowledgements not expected:\n{}".format(additional_acks))
else:
    print("No additional acknowledgement")

print("{}/{} = {}% acknowledgements received".format(rx_counter,N,100*rx_counter/N))

print()

# CRC
if len(crc_diff) > 0:
    print ("CRC difference between original message and acknowledgement in packets:\n{}".format(additional_acks))
else:
    print("No CRC difference between original messages and acknowledgements")

print()

# CR
if len(cr_diff) > 0:
    print ("CR difference between original message and acknowledgement in packets:\n{}".format(additional_acks))
else:
    print("No CR difference between original messages and acknowledgements")



