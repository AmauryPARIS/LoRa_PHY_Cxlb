import socket, json, time, argparse, random, select

IP_ADDRESS = "127.0.0.1"
PORT_NO_RX = 6790
PORT_NO_TX = 6788

node_id = "NODE_ID"

i = 1
period = 1.
TRANSMIT_WINDOW_RATIO = 1/2
RECEIVE_WINDOW_RATIO = 3/4

rx_duration = RECEIVE_WINDOW_RATIO * period
rx_counter = 0

transmit_timing = random.random() * TRANSMIT_WINDOW_RATIO * period
time.sleep(transmit_timing)

cmd_dict = {"MSG":"Packet {} from node {}".format(i, node_id)}

socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tx.connect((IP_ADDRESS, PORT_NO_TX))
socket_tx.send(bytes(json.dumps(cmd_dict), 'UTF-8'))
socket_tx.close()
cmd_dict.clear()

# Node listens for rx_duration
socket_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_rx.bind((IP_ADDRESS, PORT_NO_RX))

received_msg = {"MSG":""}



elapsed = 0
start = time.perf_counter()

while received_msg["MSG"] != "ACK-Packet {} from node {}".format(i, node_id)\
        and elapsed < rx_duration:
    ready = select.select([socket_rx],[],[],rx_duration - elapsed)
    if ready[0]:
        data, addr = socket_rx.recvfrom(1024)
        received_msg = json.loads("".join([chr(item) for item in data]))
    elapsed = time.perf_counter() - start

# If a valid acknowledgement was received, increase the rx_counter
if received_msg["MSG"] == "ACK-Packet {} from node {}".format(i, node_id):
    rx_counter += 1
    print("Ack received")

print(f"Period = {period}s")
print(f"Total elapsed time = {transmit_timing + elapsed}s\n")
if (period - transmit_timing - elapsed > 0):
    time.sleep(period - transmit_timing - elapsed)
    