import socket, json, time

print("LORA Phy layer Python Node controler - GNU Radio\n")
PORT_NO_TX = input("Enter your UDP TX port number (default = 6788): ")
if PORT_NO_TX == "":
    PORT_NO_TX = 6788
PORT_NO_RX = input("Enter your UDP RX port number (default = 6790): ")
if PORT_NO_RX == "":
    PORT_NO_RX = 6790

PORT_NO_TX = int(PORT_NO_TX)
PORT_NO_RX = int(PORT_NO_RX)

IP_ADDRESS = "127.0.0.1"

dyn_parameters = {  "CR" : "Coding Rate", 
                    "SF" : "Spreading Factor",
                    "GTX": "Gain for TX chain", 
                    "GRX": "Gain for RX chain",
                    "FTX": "USRP frequency for TX chain",
                    "FRX": "USRP frequency for RX chain",
                    "MSG": "Data to transmit",
                    "BWTX": "Bandwidth for TX chain [WORK IN PROGRESS]",
                    "BWRX": "Bandwidth for RX chain [WORK IN PROGRESS]"
                } 

out_cmd = {
                    "print" : "Print in GNURADIO current parameters"
            }

cmd_dict = {}
out_dict = {}

# Init PHY layer in GNU Radio
cmd_dict = {    #"CR" : "4", 
                #"SF" : "8",
                #"GTX": "60", 
                #"GRX": "60",
                "FTX": "910e6",
                "FRX": "900e6"
            } 
socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
socket_tx.close()
cmd_dict.clear()



for param_keys in dyn_parameters.keys():
    print(param_keys + " - " + dyn_parameters[param_keys])
for out_keys in out_cmd.keys():
    print(out_keys + " - " + out_cmd[out_keys])

print("\n")
while(True):
    cmd = str(input("Enter the parameter OR \"send\" to send all stored commands OR \"print\" to display the current parameters: "))
    if cmd == "send":
        if len(cmd_dict) != 0:
            socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
            
            socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
            start = time.perf_counter()
            socket_tx.close()
            cmd_dict.clear()

            # print("Command send to LORA physical layer in GNURADIO -------> Waiting for transmission\n")

            # socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # socket_rx.bind((IP_ADDRESS, PORT_NO_RX))
            # received = False
            
            # while not received:
            #     data, addr = socket_rx.recvfrom(1024)
            #     end = time.perf_counter()
            #     received_msg = json.loads("".join([chr(item) for item in data]))
            #     print ("Message transmited !")
            #     for key in received_msg.keys():
            #         print("     " + key + ": " + received_msg[key])
            #     print ("Elapsed time: " + str(end - start) + " [scd]")
            #     print("\n")
            #     received = True


        else:
            print("Your command list is empty\n")

    elif cmd in dyn_parameters.keys(): 
        param_value = str(input("Enter the new value of the " + dyn_parameters[cmd] + ": "))

        # Verification of the param type (int/float/etc): all parameter values should be able to be converted to an integer 
        # DONE in general_supervisor, however it doesn't show up in the upper layer terminal, only in the PHY one
        # TODO: add a way to return an error/message from the PHY layer to the upper layer (return value given through a UDP socket for example)

        cmd_dict.update({cmd:param_value})
        print("Command added to list: " + str(cmd_dict) + "\n")

    elif cmd in out_cmd.keys():
        out_dict.update({cmd:""})
        socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
        
        socket_tx.send(bytes(json.dumps(out_dict), 'UTF-8'))
        socket_tx.close()
        out_dict.clear()

    else:
        print("Unknown command, please try again\n")

