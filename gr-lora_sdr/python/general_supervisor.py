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
        source = False
        sink = False

        int_param_cmd = [
                            "CR",
                            "SF",
                        ]
        float_param_cmd = [
                            "GTX",
                            "GRX",
                            "FTX",
                            "FRX",
                            "BWTX",
                            "BWRX"
                        ]
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
            
            if cmd in float_param_cmd:
                try:
                    float(newvalue)
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

            if cmd == "GTX":
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("gain"), pmt.from_float(float(newvalue)))
                sink = True
                self.top_block.set_TX_gain(float(newvalue))
            elif cmd == "GRX":
                source_cmd = pmt.dict_add(source_cmd, pmt.intern("gain"), pmt.from_float(float(newvalue)))
                source = True
                self.top_block.set_RX_gain(float(newvalue))
            elif cmd == "FTX":
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("freq"), pmt.from_float(float(newvalue)))	
                sink = True		
                self.top_block.set_tx_freq(float(newvalue))
            elif cmd == "FRX":
                source_cmd = pmt.dict_add(source_cmd, pmt.intern("freq"), pmt.from_float(float(newvalue)))			
                source = True
                self.top_block.set_rx_freq(float(newvalue))


            # elif cmd in ["CR", "SF"]:
            #     tx_parameters += (str(cmd) + "_" + str(newvalue) + "|")
            elif cmd == "SF":
                tx_parameters += (str(cmd) + "_" + str(newvalue) + "|")
                self.top_block.set_sf(int(newvalue))
            elif cmd == "CR":
                if not int(newvalue) in range(1, 5):
                    # TODO: Add real error and way to return this error to the upper layer
                    print("ERROR: Can only set the coding rate to a integer value between 1 (corresponding to CR = 4/5) and 4 (corresponding to CR = 4/8)")
                    return 1
                tx_parameters += (str(cmd) + "_" + str(newvalue) + "|")
                self.top_block.set_cr(int(newvalue))

                # Temporary: there should be a CRTX and at least one CRRX
                # TODO: implement a way to add tags to the RX chain


            elif cmd == "BWTX":
                if not pmt.is_integer(newvalue):
                    # TODO: Add real error and way to return this error to the upper layer
                    print("ERROR: Cannot set the bandwidth to a non-integer value")
                    return 1
                self.top_block.set_bw(int(newvalue))

                # Sample rate is already set by set_bw
                # self.top_block.set_samp_rate(int(newvalue)) 

                # Prepare a BW tag
                tx_parameters += (str(cmd) + "_" + str(newvalue) + "|")

                # Debug print - TODO : erase
                print("DEBUG: BW modification added to the tx_parameters list, should be caught by tags_param_dyn and converted to a tag\n")

            elif cmd == "BWRX":
                print("ERROR: not yet implemented")


            elif cmd == "print":
                    print("FTX = " + str(self.top_block.uhd_usrp_sink_0.get_center_freq()) + "\n")
                    print("FRX = " + str(self.top_block.uhd_usrp_source_0.get_center_freq()) + "\n")
                    print("GTX = " + str(self.top_block.uhd_usrp_sink_0.get_gain()) + "\n")
                    print("GRX = " + str(self.top_block.uhd_usrp_source_0.get_gain()) + "\n")
                    print("SF = " + str(self.top_block.get_sf()) + "\n")
                    print("CR = " + str(self.top_block.get_cr()) + "\n")
            else:
                print("TX UDP General - Unknown cmd")

        if tx_parameters != "":
            self.message_port_pub(pmt.intern('GS_tx_cmd'), pmt.intern(tx_parameters))
        if sink:
            self.message_port_pub(pmt.intern('GS_sink_cmd'), sink_cmd)
        if source:
            self.message_port_pub(pmt.intern('GS_source_cmd'), source_cmd)
        if data_to_transmit:
            self.message_port_pub(pmt.intern('GS_msg'), pmt.intern(str(data_to_transmit)))


        self.consume_each(len(input_items[0]))
        return 0
