"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[],
            out_sig=[]
        )
        self.count = 0
        self.message_port_register_in(pmt.intern('MSG'))
        self.set_msg_handler(pmt.intern('MSG'), self.handle_msg)
        self.message_port_register_out(pmt.intern('MSG_out'))
    
    def handle_msg(self, msg):
        msg_out = str(pmt.to_python(msg) + "_" + str(self.count))
        self.message_port_pub(pmt.intern('MSG_out'), pmt.intern(msg_out))
        print("MSG OUT - " + str(self.count) + "\n")
        self.count += 1

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0]
        return len(output_items[0])

