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
        source = False
        sink = False

        sink_cmd = pmt.make_dict()
        source_cmd = pmt.make_dict()
        
            
        for cmd in list_cmd.keys():
            newvalue = list_cmd[cmd]
            if cmd == "GTX":
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("gain"), pmt.from_float(float(newvalue)))
                sink = True
                #self.top_block.set_TX_gain(float(newvalue))
            elif cmd == "GRX":
                source_cmd = pmt.dict_add(source_cmd, pmt.intern("gain"), pmt.from_float(float(newvalue)))
                source = True
                #self.top_block.set_RX_gain(float(newvalue))
            elif cmd == "FTX":
                sink_cmd = pmt.dict_add(sink_cmd, pmt.intern("freq"), pmt.from_float(float(newvalue)))	
                sink = True		
                #self.top_block.set_TX_freq(float(newvalue))
            elif cmd == "FRX":
                source_cmd = pmt.dict_add(source_cmd, pmt.intern("freq"), pmt.from_float(float(newvalue)))			
                source = True
                #self.top_block.set_RX_freq(float(newvalue))
            elif cmd in ["CR", "SF"]:
                tx_parameters += (str(cmd) + "_" + str(newvalue) + "|")
            elif cmd == "print":
                    print("FTX = " + str(self.top_block.uhd_usrp_sink_0.get_center_freq()) + "\n")
                    print("FRX = " + str(self.top_block.uhd_usrp_source_0.get_center_freq()) + "\n")
                    print("GTX = " + str(self.top_block.uhd_usrp_sink_0.get_gain()) + "\n")
                    print("GRX = " + str(self.top_block.uhd_usrp_source_0.get_gain()) + "\n")
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
