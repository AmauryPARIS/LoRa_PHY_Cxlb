/* -*- c++ -*- */
/* 
 * Copyright 2021 gr-lora_sdr author.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "pwr_est_impl.h"
#include <numeric>
#include <cmath>        // std::abs

namespace gr {
  namespace lora_sdr {

    pwr_est::sptr
    pwr_est::make(float samp_rate, uint32_t bandwidth, int sf, int noise_elem, int history_avg)
    {
      return gnuradio::get_initial_sptr
        (new pwr_est_impl(samp_rate, bandwidth, sf, noise_elem, history_avg));
    }

    /*
     * The private constructor
     */
    pwr_est_impl::pwr_est_impl(float samp_rate, uint32_t bandwidth, int sf, int noise_elem, int history_avg)
      : gr::sync_block("pwr_est",
              gr::io_signature::make(1,1, (1u << sf)*sizeof(gr_complex)),
              gr::io_signature::make(0, 0, 0))
    {
      m_sf                                =   sf;
      m_samp_rate                         =   samp_rate;
      m_bw                                =   bandwidth;
      m_count_noise_symbol                =   noise_elem;
      m_history_avg                       =   history_avg;
      m_margin_noise_symbol               =   10; // To avoid computing preamble symbol in noise energy (8 upchirps + 2 margin)

      m_index_history                     =   0;
      m_count_message_symbol              =   0;
      m_index_noise_sample_energy_history =   0;
      m_current_message_energy            =   0;
      m_current_noise_energy              =   0;
      m_current_snr                       =   0;
      m_msg_energy_average                =   0;
      m_snr_average                       =   0;

      m_average_computable                =   false;
      m_snr_computable                    =   false;

      m_message_energy_history.resize(m_history_avg);
      m_noise_energy_history.resize(m_history_avg);
      m_noise_sample_energy_history.resize(m_count_noise_symbol + m_margin_noise_symbol);

      m_number_of_bins     = (uint32_t)(1u << m_sf);
      m_samples_per_symbol = (uint32_t)(m_samp_rate * m_number_of_bins/ m_bw);

      message_port_register_out(pmt::mp("SNR"));
      message_port_register_out(pmt::mp("MSG_Energy"));
      message_port_register_out(pmt::mp("Noise_Energy"));
      message_port_register_out(pmt::mp("snr_avg"));
      message_port_register_out(pmt::mp("msg_avg"));
    }

    /*
     * Our virtual destructor.
     */
    pwr_est_impl::~pwr_est_impl()
    {
    }

    void pwr_est_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required){
      ninput_items_required[0] = 1;
    }

    float pwr_est_impl::compute_energy(const gr_complex *samples) {
      float energy = 0;
      std::for_each(&samples[0], &samples[m_samples_per_symbol+1], [&] (gr_complex n) {
          energy += (float) pow(pow(n.real(),2) + pow(n.imag(),2), 0.5);
      });
      return energy;
    }
    
    int pwr_est_impl::mod(int a, int b)
    {
      int r = a % b;
      return r < 0 ? r + b : r;
    }

    int
    pwr_est_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      int abs_N = 0;
      int end_N = 0;
      int i = 0;
      std::string value;
      set_tag_propagation_policy(TPP_DONT);

      
      for (size_t i = 0; i < input_items.size(); i++) {
        abs_N = nitems_read(i);
        end_N = abs_N + 1;
        tags.clear();
        get_tags_in_range(tags, 0, abs_N, end_N);
        for (it = tags.begin(); it != tags.end(); ++it) {
          
          if (pmt::symbol_to_string((*it).key) == "state"){
            value = pmt::symbol_to_string((*it).value);
            if (value == "FRAC_CFO_CORREC" || value == "SYNC"){ 
              // Message state
              m_count_message_symbol++;
              m_current_message_energy += compute_energy(in);
              
            }
            else if (value == "MSG_OVER"){ // End of message - "in" samples are noise

              // SNR COMPUTATION
              m_current_message_energy = m_current_message_energy / (m_count_message_symbol * m_samples_per_symbol);
              for (int y = m_index_noise_sample_energy_history - m_margin_noise_symbol; y < m_index_noise_sample_energy_history; y++){
                // Erase noise value that match preamble before SYNC state
                m_noise_sample_energy_history[mod(y,(m_count_noise_symbol + m_margin_noise_symbol))] = 0;
              }
              m_current_noise_energy = std::accumulate(m_noise_sample_energy_history.begin(), m_noise_sample_energy_history.end(), (float)0);
              m_current_noise_energy = m_current_noise_energy / (m_count_noise_symbol * m_samples_per_symbol);
   
              m_message_energy_history[m_index_history] = m_current_message_energy;
              m_noise_energy_history[m_index_history] = m_current_noise_energy;
              m_current_snr = 10*log(m_current_message_energy) - 10*log(m_current_noise_energy);
              message_port_pub(pmt::intern("SNR"),pmt::mp((float)m_current_snr));
              message_port_pub(pmt::intern("Noise_Energy"),pmt::mp((float)10*log(m_current_noise_energy)));
              message_port_pub(pmt::intern("MSG_Energy"),pmt::mp((float)10*log(m_current_message_energy)));

              // INDEXs UPDATE
              m_count_message_symbol = 0;
              if (m_index_history + 1 == m_history_avg){
                m_index_history = 0;
                m_average_computable = true;
              }
              else
                m_index_history++;

              // INDEXs UPDATE
              std::fill(m_noise_sample_energy_history.begin(), m_noise_sample_energy_history.end(), (float)0);

              // Average COMPUTATION
              float cum_msg_energy = 0;
              float cum_noise_energy = 0;
              if (m_average_computable) {
                for (int i = 0; i < m_history_avg; i++){
                  cum_msg_energy += m_message_energy_history[i];
                  cum_noise_energy += m_noise_energy_history[i];
                }
                m_msg_energy_average = 10*log(cum_msg_energy / m_history_avg);
                m_snr_average = m_msg_energy_average - 10*log(cum_noise_energy / m_history_avg);

                message_port_pub(pmt::intern("snr_avg"),pmt::mp((float)m_snr_average));
                message_port_pub(pmt::intern("msg_avg"),pmt::mp((float)m_msg_energy_average));
              }
              else{
                message_port_pub(pmt::intern("snr_avg"),pmt::mp((float)0));
                message_port_pub(pmt::intern("msg_avg"),pmt::mp((float)0));
              }
            }
            else {
              // Noise state
              m_index_noise_sample_energy_history = (m_index_noise_sample_energy_history + 1 == m_count_noise_symbol + m_margin_noise_symbol ? 0: m_index_noise_sample_energy_history + 1);
              m_noise_sample_energy_history[m_index_noise_sample_energy_history] = compute_energy(in);
              
            }
          }
        }
        
      }

      consume_each(1);
      return 0;
    }

  } /* namespace lora_sdr */
} /* namespace gr */

