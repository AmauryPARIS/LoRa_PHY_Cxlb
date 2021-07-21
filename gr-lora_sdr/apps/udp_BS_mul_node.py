import socket, json, time

print("LORA Phy layer Python BS controler - GNU Radio\n")

parser = argparse.ArgumentParser(description="LORA Phy layer Python Multiple Node controler - GNU Radio")

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

# Parsing
args = parser.parse_args()
cmd_dict = vars(args)

PORT_NO_TX = cmd_dict.pop('PORT_NO_TX')
PORT_NO_RX = cmd_dict.pop('PORT_NO_RX')

# PORT_NO_TX = input("Enter your UDP TX port number (default = 6788) : ")
# if PORT_NO_TX == "":
#     PORT_NO_TX = 6788
# PORT_NO_RX = input("Enter your UDP RX port number (default = 6790) : ")
# if PORT_NO_RX == "":
#     PORT_NO_RX = 6790

# PORT_NO_TX = int(PORT_NO_TX)
# PORT_NO_RX = int(PORT_NO_RX)

TIMEOUT = 60.

    # try:
    #     raw_input('Press Enter to quit: ')
    # except EOFError:
    #     pass


IP_ADDRESS = "127.0.0.1"


# Init PHY layer in GNU Radio
# cmd_dict = {    #"CR" : "4", 
#                 #"SF" : "8",
#                 #"GTX": "60", 
#                 #"GRX": "60",
#                 "FTX": "900e6",
#                 "FRX": "910e6"
#             } 
socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
socket_tx.close()
cmd_dict.clear()




print("\n")
while(True):

    # Listen for new message
    socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_rx.bind((IP_ADDRESS, PORT_NO_RX))
    print("Waiting for new received message for {}s".format(TIMEOUT))
    ready = select.select([socket_rx],[],[],TIMEOUT)
    if ready[0]:

        data, addr = socket_rx.recvfrom(1024)
        received_msg = json.loads("".join([chr(item) for item in data]))
        print("New message : \n")
        for key in received_msg.keys():
            print("     " + key + " : " + received_msg[key])
        print("\n")

        # Send ack
        print("Sending Acknowledgement")
        socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_tx.connect((IP_ADDRESS, PORT_NO_TX))

        cmd_dict = { "MSG": str("ACK-" + str(received_msg["msg"])) } 

        socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))

        socket_tx.close()
        cmd_dict.clear()
        print("\n")
    else:
        break

print("Timeout")
