import socket, json, time
import threading, argparse, select

print("LORA Phy layer Python BS controler - GNU Radio\n")

parser = argparse.ArgumentParser(description="LORA Phy layer Python Multiple Node controler - GNU Radio")

# Port numbers
parser.add_argument('--PORT_NO_TX', type = int, default=6788, help="UDP TX port number")
parser.add_argument('--PORT_NO_RX', type = int, default=6790, help="UDP RX port number")

# Physical layer parameters - to be tested
parser.add_argument('--SF-TX', type=int, help="Spreading factor", default=7)
parser.add_argument('--CR-TX', type=int, help="Coding Rate", default=4)
# parser.add_argument('--CRC-TX', type = bool, default=True, help="CRC presence")
parser.add_argument('--G-TX', type = float, default=30, help="Gain for TX chain")
parser.add_argument('--G-RX', type = float, default=20, help="Gain for RX chain")
parser.add_argument('--F-TX', type = float, default=910e6, help="USRP frequency for TX chain")
parser.add_argument('--F-RX', type = float, default=900e6, help="USRP frequency for RX chain")
# parser.add_argument('--BW-TX', type = float, default=910e6, help="Bandwidth for TX chain")
# parser.add_argument('--BW-RX', type = float, default=900e6, help="Bandwidth for RX chain")

# Parsing
args = parser.parse_args()
cmd_dict = vars(args)

PORT_NO_TX = cmd_dict.pop('PORT_NO_TX')
PORT_NO_RX = cmd_dict.pop('PORT_NO_RX')

TIMEOUT = 60.


IP_ADDRESS = "127.0.0.1"


# Init PHY layer in GNU Radio
# cmd_dict = {    #"CR-TX" : "4", 
#                 #"SF-TX" : "8",
#                 #"G-TX": "60", 
#                 #"G-RX": "60",
#                 "F-TX": "900e6",
#                 "F-RX": "910e6"
#             } 
socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
socket_tx.close()
cmd_dict.clear()


### Second version of the loop with a 2nd thread to send the message

class ThreadSend(threading.Thread):
    def __init__(self, rx_data): 
        threading.Thread.__init__(self)
        self.data = rx_data
    
    def run(self): # Sends an acknoledgment
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

socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_rx.bind((IP_ADDRESS, PORT_NO_RX))
while(True):

    # Listen for new messages for TIMEOUT seconds

    print("Waiting for a new received message for {}s".format(TIMEOUT))
    ready = select.select([socket_rx],[],[],TIMEOUT)
    if ready[0]:
        data, addr = socket_rx.recvfrom(1024)
        thread = ThreadSend(data) # New thread to send the acknowledgement 
        # -> No time spent on sending in the main thread
        thread.start()
    else:
        break

print("Timeout")
