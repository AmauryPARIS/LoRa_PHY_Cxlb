#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2021 <+YOU OR YOUR COMPANY+>.
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

class decim_factor_modifier(gr.sync_block):
    """
    docstring for block decim_factor_modifier
    """
    def __init__(self, sf=7):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name="Decim Factor Modifier",
            in_sig=[(np.complex64,2**sf)],
            out_sig=[(np.complex64,2**sf)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sf = sf
	self.startup = True

    def set_top_block(self, block):
        if self.startup:
            self.top_block = block
            self.startup = False
		

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            key = pmt.to_python(tag.key) # convert from PMT to python string
            value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
            print ("Tag key: {}; value: {}".format(key, value))
            if key == "BW-RX":
                self.top_block.set_n(self.top_block.get_samp_rate_usrp_rx()/value)
        output_items[0][:] = input_items[0]
        return len(output_items[0])