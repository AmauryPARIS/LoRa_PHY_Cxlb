#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Test Usrp Tx
# GNU Radio version: 3.7.13.5
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from hier_lora_tx import hier_lora_tx  # grc-generated hier_block
from optparse import OptionParser
import lora_sdr
import numpy
import threading
import time


class lora_test_usrp_tx(gr.top_block):

    def __init__(self, TX_freq=915e6, TX_gain=30, bw=250000, cr=4, has_crc=True, impl_head=False, mean_period_message=50, mult_const=1, sf=7):
        gr.top_block.__init__(self, "Lora Test Usrp Tx")

        ##################################################
        # Parameters
        ##################################################
        self.TX_freq = TX_freq
        self.TX_gain = TX_gain
        self.bw = bw
        self.cr = cr
        self.has_crc = has_crc
        self.impl_head = impl_head
        self.mean_period_message = mean_period_message
        self.mult_const = mult_const
        self.sf = sf

        ##################################################
        # Variables
        ##################################################
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.samp_rate = samp_rate = bw
        self.pay_len = pay_len = 32

        ##################################################
        # Blocks
        ##################################################
        self.lora_sdr_general_supervisor_0 = lora_sdr.general_supervisor()

        def _variable_function_probe_0_probe():
            while True:
                val = self.lora_sdr_general_supervisor_0.set_top_block(self)
                try:
                    self.set_variable_function_probe_0(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('', '')),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(915e6, 0)
        self.uhd_usrp_sink_0.set_gain(TX_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(bw, 0)
        self.hier_lora_tx_0 = hier_lora_tx(
            bw=bw,
            cr=cr,
            has_crc=has_crc,
            impl_head=impl_head,
            mult_const=mult_const,
            samp_rate=samp_rate,
            sf=sf,
        )
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_char*1, '127.0.0.1', 6788, 1472, True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_int*1)
        self.analog_random_source_x_0 = blocks.vector_source_i(map(int, numpy.random.randint(0, 2, 1000)), True)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_sdr_general_supervisor_0, 'GS_msg'), (self.hier_lora_tx_0, 'MSG'))
        self.msg_connect((self.lora_sdr_general_supervisor_0, 'GS_tx_cmd'), (self.hier_lora_tx_0, 'TX_cmd'))
        self.msg_connect((self.lora_sdr_general_supervisor_0, 'GS_sink_cmd'), (self.uhd_usrp_sink_0, 'command'))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_udp_source_0, 0), (self.lora_sdr_general_supervisor_0, 0))
        self.connect((self.hier_lora_tx_0, 0), (self.uhd_usrp_sink_0, 0))

    def get_TX_freq(self):
        return self.TX_freq

    def set_TX_freq(self, TX_freq):
        self.TX_freq = TX_freq

    def get_TX_gain(self):
        return self.TX_gain

    def set_TX_gain(self, TX_gain):
        self.TX_gain = TX_gain
        self.uhd_usrp_sink_0.set_gain(self.TX_gain, 0)


    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_samp_rate(self.bw)
        self.uhd_usrp_sink_0.set_bandwidth(self.bw, 0)
        self.hier_lora_tx_0.set_bw(self.bw)

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr
        self.hier_lora_tx_0.set_cr(self.cr)

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc
        self.hier_lora_tx_0.set_has_crc(self.has_crc)

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head
        self.hier_lora_tx_0.set_impl_head(self.impl_head)

    def get_mean_period_message(self):
        return self.mean_period_message

    def set_mean_period_message(self, mean_period_message):
        self.mean_period_message = mean_period_message

    def get_mult_const(self):
        return self.mult_const

    def set_mult_const(self, mult_const):
        self.mult_const = mult_const
        self.hier_lora_tx_0.set_mult_const(self.mult_const)

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.hier_lora_tx_0.set_sf(self.sf)

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.hier_lora_tx_0.set_samp_rate(self.samp_rate)

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--TX-freq", dest="TX_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set TX_freq [default=%default]")
    parser.add_option(
        "", "--TX-gain", dest="TX_gain", type="intx", default=30,
        help="Set TX_gain [default=%default]")
    parser.add_option(
        "", "--bw", dest="bw", type="intx", default=250000,
        help="Set bw [default=%default]")
    parser.add_option(
        "", "--cr", dest="cr", type="intx", default=4,
        help="Set cr [default=%default]")
    parser.add_option(
        "", "--mean-period-message", dest="mean_period_message", type="intx", default=50,
        help="Set mean_period_message [default=%default]")
    parser.add_option(
        "", "--mult-const", dest="mult_const", type="intx", default=1,
        help="Set mult_const [default=%default]")
    parser.add_option(
        "", "--sf", dest="sf", type="intx", default=7,
        help="Set sf [default=%default]")
    return parser


def main(top_block_cls=lora_test_usrp_tx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(TX_freq=options.TX_freq, TX_gain=options.TX_gain, bw=options.bw, cr=options.cr, mean_period_message=options.mean_period_message, mult_const=options.mult_const, sf=options.sf)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
