import socket, json, time

print("LORA Phy layer Python BS controler - GNU Radio\n")
PORT_NO_TX = input("Enter your UDP TX port number (default = 6788) : ")
if PORT_NO_TX == "":
    PORT_NO_TX = 6788
PORT_NO_RX = input("Enter your UDP RX port number (default = 6790) : ")
if PORT_NO_RX == "":
    PORT_NO_RX = 6790

PORT_NO_TX = int(PORT_NO_TX)
PORT_NO_RX = int(PORT_NO_RX)

IP_ADDRESS = "127.0.0.1"


# Init PHY layer in GNU Radio
cmd_dict = {    "CR" : "4", 
                "SF" : "8",
                "GTX": "60", 
                "GRX": "60",
                "FTX": "700e6",
                "FRX": "710e6"
            } 
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
