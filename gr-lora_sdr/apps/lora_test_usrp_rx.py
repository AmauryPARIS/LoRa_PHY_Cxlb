#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lora Test Usrp Rx
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from hier_lora_rx import hier_lora_rx  # grc-generated hier_block
from optparse import OptionParser
import pmt
import sip
from gnuradio import qtgui


class lora_test_usrp_rx(gr.top_block, Qt.QWidget):

    def __init__(self, TX_freq=915e6, TX_gain=30, bw=250000, cr=4, has_crc=True, hist_avg=5, noise_elem=20, sf=7, udp_rx_port=6790):
        gr.top_block.__init__(self, "Lora Test Usrp Rx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lora Test Usrp Rx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "lora_test_usrp_rx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.TX_freq = TX_freq
        self.TX_gain = TX_gain
        self.bw = bw
        self.cr = cr
        self.has_crc = has_crc
        self.hist_avg = hist_avg
        self.noise_elem = noise_elem
        self.sf = sf
        self.udp_rx_port = udp_rx_port

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = bw
        self.pay_len = pay_len = 32
        self.impl_head = impl_head = False

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccf(4, (-0.128616616593872,	-0.212206590789194,	-0.180063263231421,	3.89817183251938e-17	,0.300105438719035	,0.636619772367581	,0.900316316157106,	1	,0.900316316157106,	0.636619772367581,	0.300105438719035,	3.89817183251938e-17,	-0.180063263231421,	-0.212206590789194,	-0.128616616593872))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
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
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/opt/gr-lora_sdr/apps/output', False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.hier_lora_rx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lora_test_usrp_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_TX_freq(self):
        return self.TX_freq

    def set_TX_freq(self, TX_freq):
        self.TX_freq = TX_freq

    def get_TX_gain(self):
        return self.TX_gain

    def set_TX_gain(self, TX_gain):
        self.TX_gain = TX_gain

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_samp_rate(self.bw)
        self.hier_lora_rx_0.set_bw(self.bw)

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr
        self.hier_lora_rx_0.set_cr(self.cr)

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc
        self.hier_lora_rx_0.set_has_crc(self.has_crc)

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

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.hier_lora_rx_0.set_sf(self.sf)

    def get_udp_rx_port(self):
        return self.udp_rx_port

    def set_udp_rx_port(self, udp_rx_port):
        self.udp_rx_port = udp_rx_port
        self.hier_lora_rx_0.set_udp_rx_port(self.udp_rx_port)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.hier_lora_rx_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len
        self.hier_lora_rx_0.set_pay_len(self.pay_len)

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head
        self.hier_lora_rx_0.set_impl_head(self.impl_head)


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
        "", "--hist-avg", dest="hist_avg", type="intx", default=5,
        help="Set hist_avg [default=%default]")
    parser.add_option(
        "", "--noise-elem", dest="noise_elem", type="intx", default=20,
        help="Set noise_elem [default=%default]")
    parser.add_option(
        "", "--sf", dest="sf", type="intx", default=7,
        help="Set sf [default=%default]")
    parser.add_option(
        "", "--udp-rx-port", dest="udp_rx_port", type="intx", default=6790,
        help="Set udp_rx_port [default=%default]")
    return parser


def main(top_block_cls=lora_test_usrp_rx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(TX_freq=options.TX_freq, TX_gain=options.TX_gain, bw=options.bw, cr=options.cr, hist_avg=options.hist_avg, noise_elem=options.noise_elem, sf=options.sf, udp_rx_port=options.udp_rx_port)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
