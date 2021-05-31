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


class perf_collector(gr.basic_block):
    """
    docstring for block perf_collector
    """
    def __init__(self, sf=7, udp_rx_port=6790):
        gr.basic_block.__init__(self,
            name="perf_collector",
            in_sig=[],
            out_sig=[])

        self.SF = sf
        self.CR = 0
        self.err_corrected = 0
        self.err_detected = 0
        self.snr_avg = 0
        self.msg_avg = 0
        self.SNR = 0
        self.MSG_Energy = 0
        self.Noise_Energy = 0
        self.pay_len = 0
        self.valid_msg = False
        self.msg = False
        self.energy_ack = False
        self.msg_ack = False
        self.header_ack = False
        
        self.port_UDP = udp_rx_port

        self.message_port_register_in(pmt.intern('CR'))
        self.set_msg_handler(pmt.intern('CR'), self.CR_save)

        self.message_port_register_in(pmt.intern('err_corrected'))
        self.set_msg_handler(pmt.intern('err_corrected'), self.err_corrected_save)

        self.message_port_register_in(pmt.intern('err_detected'))
        self.set_msg_handler(pmt.intern('err_detected'), self.err_detected_save)

        self.message_port_register_in(pmt.intern('SNR'))
        self.set_msg_handler(pmt.intern('SNR'), self.SNR_save)

        self.message_port_register_in(pmt.intern('MSG_Energy'))
        self.set_msg_handler(pmt.intern('MSG_Energy'), self.MSG_Energy_save)

        self.message_port_register_in(pmt.intern('Noise_Energy'))
        self.set_msg_handler(pmt.intern('Noise_Energy'), self.Noise_Energy_save)

        self.message_port_register_in(pmt.intern('snr_avg'))
        self.set_msg_handler(pmt.intern('snr_avg'), self.snr_avg_save)

        self.message_port_register_in(pmt.intern('msg_avg'))
        self.set_msg_handler(pmt.intern('msg_avg'), self.msg_avg_save)

        self.message_port_register_in(pmt.intern('pay_len'))
        self.set_msg_handler(pmt.intern('pay_len'), self.pl_save)

        self.message_port_register_in(pmt.intern('valid_msg'))
        self.set_msg_handler(pmt.intern('valid_msg'), self.vmsg_save)

        self.message_port_register_in(pmt.intern('msg'))
        self.set_msg_handler(pmt.intern('msg'), self.msg_save)

    def CR_save(self, CR):
		self.header_ack = True
		self.CR = CR

    def err_corrected_save(self, err_corrected):
        self.err_corrected += pmt.to_python(err_corrected)

    def err_detected_save(self, err_detected):
        self.err_detected += pmt.to_python(err_detected)

    def SNR_save(self, SNR):
        self.SNR = SNR

    def MSG_Energy_save(self, MSG_Energy):
        self.MSG_Energy = MSG_Energy

    def Noise_Energy_save(self, Noise_Energy):
        self.Noise_Energy = Noise_Energy

    def snr_avg_save(self, snr_avg):
        self.energy_ack = True
        self.snr_avg = snr_avg

    def msg_avg_save(self, msg_avg):
        self.msg_avg = msg_avg

    def pl_save(self, pay_len):
        self.header_ack = True
        self.pay_len = pay_len

    def vmsg_save(self, valid_msg):
        self.valid_msg = valid_msg

    def msg_save(self, msg):
        self.msg_ack = True
        self.msg = pmt.to_python(msg)

    def send_intel(self):
        if (self.energy_ack and self.header_ack and self.msg_ack):

            received_dict = {
                "CR"        	:   str(self.CR),
                "err_corrected" :   str(self.err_corrected),
                "err_detected" 	:   str(self.err_detected),
                "SF"        	:   str(self.SF),
                "snr_avg"      	:   str(self.snr_avg),
                "msg_avg"      	:   str(self.msg_avg),
                "SNR"	    	:   str(self.SNR),
                "MSG_Energy"	:   str(self.MSG_Energy),
                "Noise_Energy"	:   str(self.Noise_Energy),
                "pay_len"   	:   str(self.pay_len),
                "msg"       	:   str(self.msg),
                "crc_valid" 	:   str(self.valid_msg)
                }
            print("RX UDP :" + str(received_dict))
            out = bytes(unicode(json.dumps(received_dict), "utf-8"))
            noutput_items = len(out)

            self.CR = 0
            self.err_corrected = 0
            self.err_detected = 0
            self.pay_len = 0
            self.snr_avg = 0
            self.msg_avg = 0
            self.SNR = 0
            self.MSG_Energy = 0
            self.Noise_Energy = 0
            self.valid_msg = False
            self.msg = False
            self.energy_ack = False
            self.msg_ack = False
            self.header_ack = False
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("127.0.0.1", self.port_UDP))
                
            s.send(out)
            s.close()
