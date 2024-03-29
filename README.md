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

This interface can be used with the [FIT/CorteXlab radiotestbed](http://www.cortexlab.fr/), in order to have a stable environment, enabling replicable experiments. A tutorial is available on [CorteXlab's Wiki](https://wiki.cortexlab.fr/doku.php?id=gnu_radio_lora_dynamic_phy_layer) and uses a [docker image](https://hub.docker.com/r/amauryparis/cxlb_lora) which includes this repository.
If you are using this docker image, all the installation steps are already executed. Thus you can go directly to the examples section.

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

Similarly to any GNU Radio OOT module, it can be built with: (It might require to use sudo depending of the installation destination)

``` bash
mkdir build
cd build
cmake ../
make
make install
```

The new blocks can be loaded in gnuradio companion by adding the following lines in `home/.gnuradio/config.conf` (If this file doesn't exist you need to create it):

``` bash
[grc]
local_blocks_path=path_to_the_downloaded_folder/gr-lora_sdr/grc
```

The hierarchical blocks `hier_rx` and `hier_tx` python files should finally be generated with GNU radio: open `hier_rx.grc` and `hier_tx.grc`, located in `gr-lora_sdr/apps`, with GNU radio companion and click the "generate the flow graph" button.

## Usage

The script `/gr-lora_sdr/apps/setpaths.sh` adds the pythonpaths required to run the generated python files for the current shell process. It has to be adapted accordingly to the installation folder, and should be executed with 
`source setpaths.sh`

### Examples

An example of a transmitter and a receiver can be found in `gr-lora_sdr/app` (both python and grc).

An example of an automated testing script and the corresponding grc and python files can also be found:

The `lora_dyn_node.py` python script runs the LoRa physical layer with a transmitter and a receiver, both connected to the JSON dynamic interface. It corresponds to the `LoRa_node.grc` GNU Radio file.

In order to show its utility, two basic python scripts are provided:

- `udp_Node.py`: UDP node python script. Sends the message given by the user
- `udp_BS.py`: UDP base station python script. Sends an acknoledgment. 
  
:warning: Both `udp_BS.py` and `udp_Node.py` have to be run with python3.

- In order to run this example you should launch 4 terminals: 2 for each USRP. 
- After connecting to the corresponding USRPs, first execute `python2 lora_dyn_node.py` on both USRP. 
  
:warning: If the USRPs are connected to the same computer, it is necessary to specify different tx and rx ports for the 2 USRPs whith the following command: `python2 lora_dyn_node.py --udp-rx-port [port_nb] --udp-tx-port [port_nb]`. If the 2 USRPs are plugged on different computers, then there is no need to do that, the default ports will be used.

- Then run `python3 udp_Node.py` on the remaining terminal for the transmitter, and `python3 udp_BS.py` on the remaining one for the receiver.

On the `udp_Node` terminal, first choose your UDP TX and RX port. If the 2 USRPs are plugged into the same computers,  use the ports specified when executing `lora-dyn-node.py`.

Then enter one of the following keywords to change the corresponding parameter if needed.

```
CR.TX - Coding Rate
SF.TX - Spreading Factor
G.TX - Gain for TX chain
G.RX - Gain for RX chain
F.TX - USRP frequency for TX chain
F.RX - USRP frequency for RX chain
MSG - Data to transmit
```

Enter the new value, then type `send` to send this new parameter to the physical layer. If a new MSG value is sent to the physical layer it is transmitted to the base station, which should respond with an acknowledgment.

More advanced upper layers are available in the `advanced_test` folder. For more information read the README located in the `advanced test` folder.




Technical report available [here](https://hal.inria.fr/hal-03465187)
