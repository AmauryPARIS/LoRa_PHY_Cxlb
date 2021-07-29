#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2021 gr-lora_sdr author.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr
import socket, pmt, json

class general_supervisor(gr.basic_block):
    """
    docstring for block general_supervisor
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="general_supervisor",
            in_sig=[np.int8],
            out_sig=[])
        
        self.startup = True
        self.top_block = None
        self.set_1 = True
	
        self.message_port_register_out(pmt.intern('GS_tx_cmd'))
        self.message_port_register_out(pmt.intern('GS_sink_cmd'))
        self.message_port_register_out(pmt.intern('GS_source_cmd'))
        self.message_port_register_out(pmt.intern('GS_msg'))
        # self.message_port_register_out(pmt.intern('GS_rx_cmd'))
    
    def set_top_block(self, block):
        if self.startup:
            self.top_block = block
            self.startup = False

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        received_msg = "".join([chr(item) for item in input_items[0]])
        print("TX UDP : " + received_msg)
        list_cmd = json.loads(received_msg)

        data_to_transmit = list_cmd.pop("MSG", False)
        tx_parameters = ""
        rx_parameters = ""
        source = False
        sink = False

        int_param_cmd = [
                            "CR.TX", # CR
                            "SF.TX", # SF
                            "CRC.TX"
                            # "CR.RX", # 0
                            # "SF.RX", # 0
                        ]
        float_param_cmd = [
                            "G.TX", # GTX
                            "G.RX", # GRX
                            "F.TX", # FTX
                            "F.RX", # FRX
                            "BW.TX", # BWTX
                            "BW.RX" # BWRX
                        ]
        # bool_param_cmd = [
        #     "CRC.TX", # 0
        # ]
        no_param_cmd = ["print"]
        str_param_cmd = ["MSG"]

        sink_cmd = pmt.make_dict()
        source_cmd = pmt.make_dict()
        
            
        for cmd in list_cmd.keys():
            newvalue = list_cmd[cmd]

            # Parameter type verification
            # TODO: Add real error and way to return this error to the upper layer

            if cmd in int_param_cmd:
                try:
                    int(newvalue)
                except ValueError:
                    print("{} value must be an integer".format(cmd))
                    print("Processing the remaining commands\n")
                    continue
            
            elif cmd in float_param_cmd:
                try:
                    newvalue = str(int(float(newvalue)))
                except ValueError:
                    print("{} value must be a float".format(cmd))
                    print("Processing the remaining commands\n")
                    continue
            
            elif cmd in str_param_cmd:
                if len(newvalue)<1:
                    print("{} value cannot be an empty string".format(cmd))
                    print("Processing the remaining commands\n")
                    continue

            elif cmd in no_param_cmd:
                if len(newvalue)>0:
                    print("{} value must be an empty string".format(cmd))
                    print("Processing the remaining commands\n")
                    continue

        ## TX cmd

            # elif cmd in ["CR", "SF"]:
            #     tx_parameters += (str(cmd) + "_" + str(newvalue) + "|")


            if cmd == "SF.TX":
                if not int(newvalue) in range(7, 13):
                    # TODO: Add real error and way to return this error to the upper layer
                    print("ERROR: Can only set the spreading factor to a integer value between 7 and 12")
                else:
                    tx_parameters += ("SF" + "_" + str(newvalue) + "|")
                
            elif cmd == "CR.TX":
                if not int(newvalue) in range(1, 5):
                    # TODO: Add real error and way to return this error to the upper layer
                    print("ERROR: Can only set the coding rate to a integer value between 1 (corresponding to CR = 4/5) and 4 (corresponding to CR = 4/8)")
                else:
                    tx_parameters += ("CR" + "_" + str(newvalue) + "|")

            elif cmd == "BW.TX":
                # self.top_block.set_bw_tx(float(newvalue))

                # Sample rate is already set by set_bw
                # self.top_block.set_samp_rate(int(newvalue)) 

                # Prepare a BW tag
                tx_parameters += ("BW_" + str(newvalue) + "|")
                
                # Update USRP BW
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("bandwidth"), pmt.from_float(float(newvalue)))
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("rate"), pmt.from_float(float(newvalue)))                
                sink = True

            elif cmd == "CRC.TX":
                if not int(newvalue) in [0, 1]:
                    # TODO: Add real error and way to return this error to the upper layer
                    print("ERROR: Can only set the CRC presence to 0 (false) or 1 (true)")
                    return 1
                else:
                    tx_parameters += ("CRC" + "_" + str(newvalue) + "|")
          

        ## RX cmd
            elif cmd == "BW.RX":
                # self.top_block.set_bw_rx(float(newvalue))

                # Sample rate variable (not the tag) is already set by set_bw
                # self.top_block.set_samp_rate(int(newvalue))

                # Prepare a BW tag
                rx_parameters += ("BW" + "_" + str(newvalue) + "|")

                # Debug print - TODO : erase
                print("DEBUG: BW modification added to the rx_parameters list, should be caught by tags_param_dyn and converted to a tag\n")

            
            # No RX SF control is possible for now

        # USRP cmd
            elif cmd == "G.TX":
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("gain"), pmt.from_float(float(newvalue)))
                sink = True
                # self.top_block.set_TX_gain(float(newvalue))
            elif cmd == "G.RX":
                source_cmd = pmt.dict_add(source_cmd, pmt.intern("gain"), pmt.from_float(float(newvalue)))
                source = True
                # self.top_block.set_RX_gain(float(newvalue))
            elif cmd == "F.TX":
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("freq"), pmt.from_float(float(newvalue)))	
                sink = True		
                # self.top_block.set_tx_freq(float(newvalue))
            elif cmd == "F.RX":
                source_cmd = pmt.dict_add(source_cmd, pmt.intern("freq"), pmt.from_float(float(newvalue)))			
                source = True
                # self.top_block.set_rx_freq(float(newvalue))

        # print
            elif cmd == "print":
                print("F.TX = " + str(self.top_block.uhd_usrp_sink_0.get_center_freq()))
                # print("tx_freq variable = " + str(self.top_block.get_tx_freq()) + "\n")
                print("F.RX = " + str(self.top_block.uhd_usrp_source_0.get_center_freq()) + "\n")
                # print("rx_freq variable = " + str(self.top_block.get_rx_freq()) + "\n")
                
                print("G.TX = " + str(self.top_block.uhd_usrp_sink_0.get_gain()))
                print("G.RX = " + str(self.top_block.uhd_usrp_source_0.get_gain()) + "\n")
                
                # print("SF.TX = " + str(self.top_block.get_sf_tx()))
                # print("SF.RX = " + str(self.top_block.get_sf_rx()) + "\n")

                # print("CR.TX = " + str(self.top_block.get_cr_tx()) )
                # print("CR.RX = " + str(self.top_block.get_cr_rx()) + "\n")

                # print("BW.TX = " + str(self.top_block.get_bw_tx()))
                # print("BW.RX = " + str(self.top_block.get_bw_rx()) + "\n")

                # print("CRC.TX = " + str(self.top_block.get_has_crc_tx()))
                # print("CRC.RX = " + str(self.top_block.get_has_crc_rx()) + "\n")
            else:
                print("TX UDP General - Unknown cmd")

        if tx_parameters != "":
            self.message_port_pub(pmt.intern('GS_tx_cmd'), pmt.intern(tx_parameters))
        # if rx_parameters != "":
        #     self.message_port_pub(pmt.intern('GS_rx_cmd'), pmt.intern(rx_parameters))        
        if sink:
            self.message_port_pub(pmt.intern('GS_sink_cmd'), sink_cmd)
        if source:
            self.message_port_pub(pmt.intern('GS_source_cmd'), source_cmd)
        if data_to_transmit:
            self.message_port_pub(pmt.intern('GS_msg'), pmt.intern(str(data_to_transmit)))


        self.consume_each(len(input_items[0]))
        return 0
