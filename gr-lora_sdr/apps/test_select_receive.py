import socket, json, time
import threading, argparse, select


IP_ADDRESS = "127.0.0.1"
PORT_NO_TX = 6790
PORT_NO_RX = 6788

TIMEOUT = 60.


print("\n")
socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_rx.bind((IP_ADDRESS, PORT_NO_RX))
while(True):

    # Listen for new message

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

        cmd_dict = { "MSG": str("ACK-" + str(received_msg["MSG"])) } 

        socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))

        socket_tx.close()
        cmd_dict.clear()
        print("\n")
    else:
        break

print("Timeout")