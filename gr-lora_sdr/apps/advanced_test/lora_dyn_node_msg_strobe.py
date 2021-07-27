#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Dyn Node Msg Strobe
# GNU Radio version: 3.7.13.5
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from hier_lora_rx import hier_lora_rx  # grc-generated hier_block
from hier_lora_tx import hier_lora_tx  # grc-generated hier_block
from optparse import OptionParser
import epy_block_0
import lora_sdr
import pmt
import threading
import time


class lora_dyn_node_msg_strobe(gr.top_block):

    def __init__(self, hist_avg=5, noise_elem=20, rx_freq=915e6, sf=7, tx_freq=915e6, udp_rx_port=6790, udp_tx_port=6788):
        gr.top_block.__init__(self, "Lora Dyn Node Msg Strobe")

        ##################################################
        # Parameters
        ##################################################
        self.hist_avg = hist_avg
        self.noise_elem = noise_elem
        self.rx_freq = rx_freq
        self.sf = sf
        self.tx_freq = tx_freq
        self.udp_rx_port = udp_rx_port
        self.udp_tx_port = udp_tx_port

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = 250000
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.samp_rate = samp_rate = bw
        self.pay_len = pay_len = 32
        self.mult_const = mult_const = 1
        self.impl_head = impl_head = False
        self.has_crc = has_crc = True
        self.cr = cr = 4
        self.TX_gain = TX_gain = 30

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

        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('', '')),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(rx_freq, 0)
        self.uhd_usrp_source_0.set_gain(20, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_bandwidth(bw, 0)
        self.uhd_usrp_source_0.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_0.set_auto_iq_balance(True, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('', '')),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(tx_freq, 0)
        self.uhd_usrp_sink_0.set_gain(TX_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(bw, 0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccf(4, (-0.128616616593872,	-0.212206590789194,	-0.180063263231421,	3.89817183251938e-17	,0.300105438719035	,0.636619772367581	,0.900316316157106,	1	,0.900316316157106,	0.636619772367581,	0.300105438719035,	3.89817183251938e-17,	-0.180063263231421,	-0.212206590789194,	-0.128616616593872))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.hier_lora_tx_0 = hier_lora_tx(
            bw=bw,
            cr=cr,
            has_crc=has_crc,
            impl_head=impl_head,
            mult_const=mult_const,
            samp_rate=samp_rate,
            sf=sf,
        )
        self.hier_lora_rx_0 = hier_lora_rx(
            bw=bw,
            cr=cr,
            has_crc=has_crc,
            hist_avg=hist_avg,
            impl_head=impl_head,
            noise_elem=noise_elem,
            pay_len=pay_len,
            samp_rate=samp_rate,
            sf=sf,
            udp_rx_port=udp_rx_port,
        )
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_char*1, '127.0.0.1', udp_tx_port, 1472, True)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_0, 'MSG'))
        self.msg_connect((self.epy_block_0, 'MSG_out'), (self.hier_lora_tx_0, 'MSG'))
        self.msg_connect((self.lora_sdr_general_supervisor_0, 'GS_msg'), (self.hier_lora_tx_0, 'MSG'))
        self.msg_connect((self.lora_sdr_general_supervisor_0, 'GS_tx_cmd'), (self.hier_lora_tx_0, 'TX_cmd'))
        self.msg_connect((self.lora_sdr_general_supervisor_0, 'GS_sink_cmd'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.lora_sdr_general_supervisor_0, 'GS_source_cmd'), (self.uhd_usrp_source_0, 'command'))
        self.connect((self.blocks_udp_source_0, 0), (self.lora_sdr_general_supervisor_0, 0))
        self.connect((self.hier_lora_tx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.hier_lora_rx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.interp_fir_filter_xxx_0, 0))

    def get_hist_avg(self):
        return self.hist_avg

    def set_hist_avg(self, hist_avg):
        self.hist_avg = hist_avg
        self.hier_lora_rx_0.set_hist_avg(self.hist_avg)

    def get_noise_elem(self):
        return self.noise_elem

    def set_noise_elem(self, noise_elem):
        self.noise_elem = noise_elem
        self.hier_lora_rx_0.set_noise_elem(self.noise_elem)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.uhd_usrp_source_0.set_center_freq(self.rx_freq, 0)

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.hier_lora_tx_0.set_sf(self.sf)
        self.hier_lora_rx_0.set_sf(self.sf)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.uhd_usrp_sink_0.set_center_freq(self.tx_freq, 0)

    def get_udp_rx_port(self):
        return self.udp_rx_port

    def set_udp_rx_port(self, udp_rx_port):
        self.udp_rx_port = udp_rx_port
        self.hier_lora_rx_0.set_udp_rx_port(self.udp_rx_port)

    def get_udp_tx_port(self):
        return self.udp_tx_port

    def set_udp_tx_port(self, udp_tx_port):
        self.udp_tx_port = udp_tx_port

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_samp_rate(self.bw)
        self.uhd_usrp_source_0.set_bandwidth(self.bw, 0)
        self.uhd_usrp_source_0.set_bandwidth(self.bw, 1)
        self.uhd_usrp_sink_0.set_bandwidth(self.bw, 0)
        self.hier_lora_tx_0.set_bw(self.bw)
        self.hier_lora_rx_0.set_bw(self.bw)

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.hier_lora_tx_0.set_samp_rate(self.samp_rate)
        self.hier_lora_rx_0.set_samp_rate(self.samp_rate)

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len
        self.hier_lora_rx_0.set_pay_len(self.pay_len)

    def get_mult_const(self):
        return self.mult_const

    def set_mult_const(self, mult_const):
        self.mult_const = mult_const
        self.hier_lora_tx_0.set_mult_const(self.mult_const)

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head
        self.hier_lora_tx_0.set_impl_head(self.impl_head)
        self.hier_lora_rx_0.set_impl_head(self.impl_head)

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc
        self.hier_lora_tx_0.set_has_crc(self.has_crc)
        self.hier_lora_rx_0.set_has_crc(self.has_crc)

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr
        self.hier_lora_tx_0.set_cr(self.cr)
        self.hier_lora_rx_0.set_cr(self.cr)

    def get_TX_gain(self):
        return self.TX_gain

    def set_TX_gain(self, TX_gain):
        self.TX_gain = TX_gain
        self.uhd_usrp_sink_0.set_gain(self.TX_gain, 0)



def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--hist-avg", dest="hist_avg", type="intx", default=5,
        help="Set hist_avg [default=%default]")
    parser.add_option(
        "", "--noise-elem", dest="noise_elem", type="intx", default=20,
        help="Set noise_elem [default=%default]")
    parser.add_option(
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set rx_freq [default=%default]")
    parser.add_option(
        "", "--sf", dest="sf", type="intx", default=7,
        help="Set sf [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set tx_freq [default=%default]")
    parser.add_option(
        "", "--udp-rx-port", dest="udp_rx_port", type="intx", default=6790,
        help="Set udp_rx_port [default=%default]")
    parser.add_option(
        "", "--udp-tx-port", dest="udp_tx_port", type="intx", default=6788,
        help="Set udp_tx_port [default=%default]")
    return parser


def main(top_block_cls=lora_dyn_node_msg_strobe, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(hist_avg=options.hist_avg, noise_elem=options.noise_elem, rx_freq=options.rx_freq, sf=options.sf, tx_freq=options.tx_freq, udp_rx_port=options.udp_rx_port, udp_tx_port=options.udp_tx_port)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
