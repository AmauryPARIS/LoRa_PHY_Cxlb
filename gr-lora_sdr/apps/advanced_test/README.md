# Advanced tests

This folder contains more advanced upper layers comparing to `udp_Node.py` and `udp_BS.py` in the parent `apps` folder.

Each subfolder contains one Base Station upper layer and one node upper layer.

## Multiple nodes

In the `mul_node` folder, the base station is _almost_ always listening for new received messages. For each received message, it sends an acknoledgement.

The node periodically sends N messages during a transmitting window and then listens for a short period of time in order to receive the acknoledgement.
The message emission can either be always at the start of the transmitting window, or randomly in this window.

Both the BS and the node are highly customizable: all TX parameters can be adjusted through flags when launching the script.

They can be used to test the PHY parameters dynamism, as well as to generate interference when launching the `udp_mul_node.py` script on several nodes.

## Automate

The `automate` folder contains scripts that are adapted from the `mul_node` folder, but conceived to be easier to automate with a task file and deploy them on CorteXlab.

## Parameter testing

Finally, the `param_test` folder helps to test all PHY parameters dynamism, thanks to a given scenario where the scripts knows which acknoledgments it should receive or not. At the end of the scripts, the `udp_node_param_test.py` script prints out the missing/additional acknoledgments, as well as the acknoledgemnts where the CR or CRC parameters were not identical to the corresponding transmitted message.
