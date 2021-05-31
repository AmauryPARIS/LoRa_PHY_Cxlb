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

#ifndef INCLUDED_LORA_SDR_PWR_EST_IMPL_H
#define INCLUDED_LORA_SDR_PWR_EST_IMPL_H

#include <lora_sdr/pwr_est.h>

namespace gr {
  namespace lora_sdr {

    class pwr_est_impl : public pwr_est
    {
     private:
      int m_sf; // Spreading factor
      float m_samp_rate; // Sample rate
      int m_bw; // Bandwidth
      int m_count_noise_symbol; // Number of noise measurement to save to compute the noise energy after one message
      int m_history_avg; // Number of message/noise energy measurement to keep for average (AVG) computation 
      int m_index_history; // Index to save value in m_message_energy_history and m_noise_energy_history
      int m_count_message_symbol; // Index to keep track of the number of symbol in the current message 
      int m_index_noise_sample_energy_history; // Index to save m_noise_elem number of noise measurement before one message
      float m_current_message_energy; // energy value for the demodulated message
      float m_current_noise_energy; // energy value for noise after last demodulated message
      float m_current_snr; // SNR value for the last demodulated message
      float m_msg_energy_average; // MSG energy average value for the last m_history_avg messages
      float m_snr_average; // SNR average value for the last m_history_avg messages
      int m_margin_noise_symbol; // To avoid computing preamble symbol in noise energy. Set to 10 (8 upchirps + 2 margin). Need to be updated if change in preamble

      bool m_average_computable; // Indicate if enough SNR values have been computed to calculate average
      bool m_snr_computable; // Indicate if enough noise values have been computed to calculate SNR

      uint32_t m_number_of_bins;
      uint32_t m_samples_per_symbol;

      std::vector<float> m_message_energy_history; // m_history_avg past value of message energy
      std::vector<float> m_noise_energy_history; // m_history_avg past value of noise energy
      std::vector<float> m_noise_sample_energy_history; // history of noise sample to comput SNR after one message is received

      std::vector<tag_t> tags;
      std::vector<tag_t>::iterator it;

      float compute_energy(const gr_complex *samples);
      int mod(int a, int b);
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

     public:
      pwr_est_impl(float samp_rate, uint32_t bandwidth, int sf, int noise_elem, int history_avg);
      ~pwr_est_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace lora_sdr
} // namespace gr

#endif /* INCLUDED_LORA_SDR_PWR_EST_IMPL_H */

