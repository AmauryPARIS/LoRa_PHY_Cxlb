# LoRa_PHY_Cxlb

Dynamic and customizable LoRa physical layer, derived  from  the  [original  EPFL  LoRa  implementation](https://www.epfl.ch/labs/tcl/resources-and-sw/lora-phy/) in GNU Radio. More information on this implementation can be found in "Dynamic LoRa PHY layer for MAC experimentation using FIT/CorteXlab testbed", written by Amaury Paris, Leonardo S. Cardoso and Jean-Marie Gorce.

This adaptation allows end-users to connect any existing upper layer to the physical layer through an easy to use interface using the JSON format, without having to implement the upper layer in GNU Radio.

## Features

- USRP ⟷ USRP transmissions
- USRP ⟷ commercial LoRa transceiver transmissions

- Modifying the following parameters:
  - Spreading factors: 7-12 (without reduced rate mode)
  - Coding rates: 0-4
  - Gain for RX and TX chains 
  - RX and TX frequencies

- Payload length: up to LoRa maximum packet length (255 Bytes)

- Verification of payload CRC
- Verification of explicit header checksum
- Implicit and explicit header mode (modification inside .grc file needed)

This interface can be used with the [FIT/CorteXlab radiotestbed](http://www.cortexlab.fr/), in order to have a stable environment, enabling replicable experiments.

## Requirements

- Gnuradio 3.7
- python 2
- python 3
- cmake
- swig
- libvolk
- UHD

If not explicitly mentioned, all python scripts should be run with python2.

## Installation

The installation path can be set in `CMakeLists.txt` under `#set destination`.(default: `home/lora_sdr`)

Similarly to any GNU Radio OOT module, it can be build with: (It might require to use sudo depending of the installation destination)
```sh
mkdir build
cd build
cmake ../
make
make install
```

The new blocks can be loaded in gnuradio companion by adding the following lines in `home/.gnuradio/config.conf` (If this file doesn't exist you need to create it):

```
[grc]
local_blocks_path=path_to_the_downloaded_folder/gr-lora_sdr/grc
```

The hierarchical blocks `hier_rx` and `hier_tx` python files should finally be generated with GNU radio: open `hier_rx.grc` and `hier_tx.grc`, located in `gr-lora_sdr/apps`, with GNU radio companion and click the "generate the flow graph" button.

## Usage
The script `/gr-lora_sdr/apps/setpaths.sh` adds the pythonpaths required to run the generated python files for the current shell process. It has to be addapted accordingly to the installation folder, and should be executed with 
`source setpaths.sh`

### Examples
An example of a transmitter and a receiver can be found in `gr-lora_sdr/app` (both python and grc).

An example of an automated testing script and the corresponding grc and python file can also be found:

- The `lora_dyn_node.py` python script runs the LoRa physical layer with a transmitter and a receiver, both connected to the JSON dynamic interface.  
- It can be used alongside the `udp_Node.py` (UDP node python script, which sends the message given by the user), or the `udp_BS.py` (UDP base station python script, which sends an acknoledgment). `udp_BS.py` and `udp_Node.py` have to be run with python3.
- In order to run the example you should launch 4 terminals: 2 for each USRP. 
- After connecting to the corresponding USRPs, first execute `python2 lora_dyn_node.py` on both USRP. Then run `python3 udp_Node.py` on the remaining terminal for the transmitter, and `python3 udp_BS.py` on the remaining one for the receiver.

On the `udp_Node` terminal, first choose your UDP TX and RX port. Then enter one of the following keywords to change the corresponding parameter if needed.

```
CR - Coding Rate
SF - Spreading Factor
GTX - Gain for TX chain
GRX - Gain for RX chain
FTX - USRP frequency for TX chain
FRX - USRP frequency for RX chain
MSG - Data to transmit
```

Enter the new value, then type `send` to send this new parameter to the physical layer. If a new MSG value is sent to the physical layer it is transmitted to the base station, which should respond with an acknowledgment.
