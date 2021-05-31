/* -*- c++ -*- */
/* 
 * Copyright 2020 me.
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

#ifndef INCLUDED_LORA_SDR_POINT_TO_POINT_IMPL_H
#define INCLUDED_LORA_SDR_POINT_TO_POINT_IMPL_H

#include <lora_sdr/point_to_point.h>
#include <map>

namespace gr {
  namespace lora_sdr {

    class point_to_point_impl : public point_to_point
    {
     private:
      int m_node_id; // ID of this node in the network
      int m_sending_period; // Time in ms between each transmission
      pmt::pmt_t m_message; // Msg to be send
      int m_pay_len; // Size of the payload 
      int m_waiting_ack_time; // Time to wait before acknoledge a message 
      bool m_gateway; // If this is not a full mesh network, indicate if this node has to act as the gateway
      bool m_full_mesh; // Indicate if the node must send its message to every node, or only to the gateway (if it is not itself)
      const int m_BROADCAST_ID = 666; // Used as a dest_id when the message is to be broadcast
      const int m_GATEWAY_ID = 777; // Used as a dest_id when the message is to be broadcast
      int m_count_msg; // Keep count of the number of send message, also used as an ID for every send message
      bool m_WAIT_ACK; // Indicate if we want to wait for the ack of a message before sending a new one
      std::map<int, bool> m_msg_history; // Keep track of every send message with [msg_id][acked bool]
      std::list<int> m_node_history; // Keep track of every node on the network. The bool was for if its the gateway, change the map to a list

      void send(pmt::pmt_t msg, int dest_id);
      void trigger_msg_handler(pmt::pmt_t msg);
      void received_msg_handler(pmt::pmt_t msg);
      void msg_to_be_acked();
      void msg_ack(int msg_id);
      void print_stats(pmt::pmt_t msg);



     public:
      point_to_point_impl(int node_id, int pay_len, int waiting_ack_time, bool gateway, bool full_mesh, bool WAIT_ACK);
      ~point_to_point_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace lora_sdr
} // namespace gr

#endif /* INCLUDED_LORA_SDR_POINT_TO_POINT_IMPL_H */

