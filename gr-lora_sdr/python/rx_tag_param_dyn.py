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

import numpy
from gnuradio import gr
import pmt

class rx_tag_param_dyn(gr.sync_block):
    """
    Converts the RX commands given as a message into tags that are added to the data stream.
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="rx_tag_param_dyn",
            in_sig=[numpy.complex64],
            out_sig=[numpy.complex64])
        
        self.rx_cmd = []

        self.message_port_register_in(pmt.intern('RX_cmd'))
        self.set_msg_handler(pmt.intern('RX_cmd'), self.handle_cmd)

    def handle_cmd(self, msg):
        start = 0
        msg_str = pmt.to_python(msg)
        while msg_str.find("|", start, len(msg_str)) != -1:
            cmd = msg_str[start:msg_str.find("|", start, len(msg_str))]
            self.rx_cmd.append(cmd)
            start = msg_str.find("|", start, len(msg_str))+1

    def work(self, input_items, output_items):
        offset = self.nitems_written(0)
        for cmd in self.rx_cmd:
            underscoreposition = cmd.find("_")
            parameter = pmt.intern(cmd[0:underscoreposition])
            value = pmt.intern(cmd[underscoreposition+1:len(cmd)])
            self.add_item_tag(0, offset, parameter, value)
            print("DEBUG Tag: {} - Value: {}".format(parameter, value))

        self.rx_cmd = []

        output_items[0][:] = input_items[0]
        return len(output_items[0])

