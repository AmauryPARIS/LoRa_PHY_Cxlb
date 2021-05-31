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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <chrono>
#include <thread>

#include <gnuradio/io_signature.h>
#include "point_to_point_impl.h"

namespace gr {
  namespace lora_sdr {

    point_to_point::sptr
    point_to_point::make(int node_id, int pay_len, int waiting_ack_time, bool gateway, bool full_mesh, bool WAIT_ACK)
    {
      return gnuradio::get_initial_sptr
        (new point_to_point_impl(node_id, pay_len, waiting_ack_time, gateway, full_mesh, WAIT_ACK));
    }

    /*
     * The private constructor
     */
    point_to_point_impl::point_to_point_impl(int node_id, int pay_len, int waiting_ack_time, bool gateway, bool full_mesh, bool WAIT_ACK)
      : gr::sync_block("point_to_point",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {
      m_node_id = node_id;
      m_pay_len = pay_len;
      m_waiting_ack_time = waiting_ack_time;
      m_gateway = gateway;
      m_full_mesh = full_mesh;
      m_count_msg = 0;
      m_WAIT_ACK = WAIT_ACK;

      if (m_gateway == true){
        m_node_id = m_GATEWAY_ID;
      }

      message_port_register_in(pmt::mp("received_msg"));
      set_msg_handler(pmt::mp("received_msg"),boost::bind(&point_to_point_impl::received_msg_handler, this, _1));

      message_port_register_in(pmt::mp("trigger_msg"));
      set_msg_handler(pmt::mp("trigger_msg"),boost::bind(&point_to_point_impl::trigger_msg_handler, this, _1));

      message_port_register_in(pmt::mp("trigger_stats"));
      set_msg_handler(pmt::mp("trigger_stats"),boost::bind(&point_to_point_impl::print_stats, this, _1));

      message_port_register_out(pmt::mp("msg"));
    }

    /*
     * Our virtual destructor.
     */
    point_to_point_impl::~point_to_point_impl()
    {
    }

    void point_to_point_impl::send(pmt::pmt_t msg, int dest_id){

      std::string msg_with_header = "" + std::to_string(dest_id) + "_" + std::to_string(m_node_id) + "_" + std::to_string(m_count_msg) + "_" + pmt::symbol_to_string(msg) + "_";
      while (msg_with_header.size() != m_pay_len){
        msg_with_header += "0"; // Add zeros to reach the wanted payload length
      }
      message_port_pub(pmt::intern("msg"),pmt::mp(msg_with_header));
      std::cout << "[TX] Message " << std::to_string(m_count_msg) << " send to " << std::to_string(dest_id) << " : " << msg_with_header << "\n";
      m_count_msg += 1;
    }

    void point_to_point_impl::trigger_msg_handler(pmt::pmt_t msg){
      if (m_gateway != true){ // 
        int dest_id;
        srand (time(NULL));
        if (m_full_mesh){
          if (m_node_history.size() == 0 || m_count_msg == 0){
            dest_id = m_BROADCAST_ID; // Send its first messages to every one for discovery purpose
          }
          else{
            int node_id_rand_position = rand() % m_node_history.size(); // Send its message to a random node in the network 
            auto vi = m_node_history.begin();
            std::advance(vi, node_id_rand_position);
            dest_id = *vi;
          }
        }
        else{
          dest_id = m_GATEWAY_ID; // Send its message to the gateway
        }
        
        if (m_WAIT_ACK == true && m_msg_history[m_count_msg] == false && m_count_msg != 0){
          std::cout << "[TX] New message blocked - Previous message " << std::to_string(m_count_msg) << " not acked \n";
          return; // Wait for the previous message to be acked before sending a new one
        }

        msg_to_be_acked();
        send(msg,dest_id);
      } 
    }

    void point_to_point_impl::received_msg_handler(pmt::pmt_t msg){

      // Unwrap the message 
      std::string msg_with_header = pmt::symbol_to_string(msg);
      int delimiter_one = msg_with_header.find("_");
      int delimiter_two = msg_with_header.find("_", delimiter_one + 1);
      int delimiter_three = msg_with_header.find("_", delimiter_two + 1);
      int delimiter_four = msg_with_header.find("_", delimiter_three + 1);

      if (delimiter_one == -1 || delimiter_two == -1 || delimiter_three == -1 || delimiter_four == -1){
        std::cout << "[RX] Message " << msg_with_header << " is not valid \n";
        return; // The frame structure is invalid and all components could not be found
      }

      int msg_dest_id = std::stoi(msg_with_header.substr(0,delimiter_one));
      int msg_node_id = std::stoi(msg_with_header.substr(delimiter_one+1,delimiter_two - delimiter_one));
      int msg_content_id = std::stoi(msg_with_header.substr(delimiter_two+1,delimiter_three - delimiter_two));
      std::string msg_content = msg_with_header.substr(delimiter_three+1,delimiter_four - delimiter_three -1);

      std::cout << "[RX] Message " << std::to_string(msg_content_id) << " received from " << std::to_string(msg_node_id) << " : " << msg_content << " ";

      // If the message is intended for this node
      if ((msg_dest_id == m_node_id || msg_dest_id == m_BROADCAST_ID) && (msg_node_id != m_node_id)){
      //if (msg_dest_id == m_node_id || msg_dest_id == m_BROADCAST_ID){
        std::cout << "| Processed | \n";
        std::this_thread::sleep_for(std::chrono::milliseconds(m_waiting_ack_time));
        
        // Type of message [Content vs ACK]
        if (msg_content.substr(0,3) == "ACK"){
          msg_ack(std::stoi(msg_content.substr(4,msg_content.length()-4)));
        }
        else{
          send(pmt::string_to_symbol("ACK-" + std::to_string(msg_content_id)),msg_node_id);
        }
      }
      else{
        std::cout << "| Not Processed | \n";
      }
      // Known node ? ;
      if (std::find(m_node_history.begin(), m_node_history.end(), msg_node_id) == m_node_history.end() && msg_node_id != m_node_id){
        m_node_history.push_back(msg_node_id);
      }
      if (std::find(m_node_history.begin(), m_node_history.end(), msg_dest_id) == m_node_history.end() && msg_node_id != m_node_id){
        m_node_history.push_back(msg_dest_id);
      }

    }

    void point_to_point_impl::msg_to_be_acked(){
      m_msg_history[m_count_msg] = false;
    }

    void point_to_point_impl::msg_ack(int msg_id){
      if ( m_msg_history.find(msg_id) == m_msg_history.end() ) {
        std::cout << "[ACK] Message " << std::to_string(msg_id) << " not in tracking list\n";
      } else {
        m_msg_history[msg_id] = true;
        std::cout << "[ACK] Message " << std::to_string(msg_id) << " acked in tracking list\n";
      }
      
    }

    void point_to_point_impl::print_stats(pmt::pmt_t msg){
      int count_total_message = 0;
      int count_nack_message = 0;
      for (std::map<int,bool>::iterator it=m_msg_history.begin(); it!=m_msg_history.end(); ++it){
        if (it->second == false)
          count_nack_message += 1;
        count_total_message += 1;
      }
      float success_percentage = (float)100 - (((float)count_nack_message / (float)count_total_message) * 100);
      std::cout << "[STATS] Transmission stat " << std::to_string(success_percentage) << "% ack over " << std::to_string(count_total_message) << " messages \n";

      std::cout << "[STATS] List of known nodes \n";
      if (m_full_mesh == true){
        for (std::list<int>::iterator it=m_node_history.begin(); it!=m_node_history.end(); ++it)
          std::cout << "" << std::to_string(*it) << " # ";
      }
      std::cout << "\n";
    }

    int
    point_to_point_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      return 0;
    }

  } /* namespace lora_sdr */
} /* namespace gr */

