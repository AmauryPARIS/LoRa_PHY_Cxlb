#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "hamming_enc_impl.h"
#include <lora_sdr/utilities.h>

namespace gr {
  namespace lora_sdr {

    hamming_enc::sptr
    hamming_enc::make(uint8_t cr, uint8_t sf)
    {
      return gnuradio::get_initial_sptr
        (new hamming_enc_impl(cr, sf));
    }


    /*
     * The private constructor
     */
    hamming_enc_impl::hamming_enc_impl(uint8_t cr, uint8_t sf)
      : gr::sync_block("hamming_enc",
              gr::io_signature::make(1,1, sizeof(uint8_t)),
              gr::io_signature::make(1,1, sizeof(uint8_t)))
    {
        m_cr = cr;
        m_sf = sf;
    }

    /*
     * Our virtual destructor.
     */
    hamming_enc_impl::~hamming_enc_impl()
    {}

    int
    hamming_enc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const uint8_t *in_data = (const uint8_t *) input_items[0];
      uint8_t *out = (uint8_t *) output_items[0];

      uint64_t abs_N, end_N;
      set_tag_propagation_policy(TPP_DONT);
      
      for (size_t i = 0; i < input_items.size(); i++) {
        abs_N = nitems_read(i);
        end_N = abs_N + noutput_items;
        tags.clear();
        get_tags_in_range(tags, 0, abs_N, end_N);
        for (it = tags.begin(); it != tags.end(); ++it) {
          key = pmt::symbol_to_string((*it).key);
          value = stoi(pmt::symbol_to_string((*it).value));

          if (key == "CR-TX"){ 
            m_cr = value;
            // std::cout << "Hamming imp - New CR : " << value << "\n";
          }
          if (key == "SF-TX"){
            m_sf = value;
            // std::cout << "Hamming imp - New SF : " << value << "\n";
          }
        }
        
      }


      std::vector<bool> data_bin;
      bool p0,p1,p2,p3,p4;
      for(int i=0; i<noutput_items;i++){
          #ifdef GRLORA_DEBUG
          std::cout<<std::hex<<(int)in_data[i]<<"   ";
          #endif
          uint8_t cr_app=(i<m_sf-2)?4:m_cr;
          data_bin = int2bool(in_data[i],4);

          //the data_bin is msb first
          if(cr_app != 1){ //need hamming parity bits
              p0=data_bin[3]^data_bin[2]^data_bin[1];
              p1=data_bin[2]^data_bin[1]^data_bin[0];
              p2=data_bin[3]^data_bin[2]^data_bin[0];
              p3=data_bin[3]^data_bin[1]^data_bin[0];
              //we put the data LSB first and append the parity bits
              out[i]=(data_bin[3]<<7|data_bin[2]<<6|data_bin[1]<<5|data_bin[0]<<4|p0<<3|p1<<2|p2<<1|p3)>>(4-cr_app);

          }
          else{// coding rate = 4/5 we add a parity bit
              p4=data_bin[0]^data_bin[1]^data_bin[2]^data_bin[3];
              out[i]=(data_bin[3]<<4|data_bin[2]<<3|data_bin[1]<<2|data_bin[0]<<1|p4);
          }
          #ifdef GRLORA_DEBUG
             std::cout<<std::hex<<(int)out[i]<<std::dec<<std::endl;
          #endif
      }
      
      // std::cout << "hamming len : " << (int)(out[0]<<4)+out[1] <<  "\n";
      // PROPAGATE TAGS WITH NEW OFFSET
      for (it = tags.begin(); it != tags.end(); ++it) {
        tag_t tag;
        tag.offset = nitems_written(0);
        tag.key = it->key;
        tag.value = it->value;
        add_item_tag(0, tag); 
      }
      return noutput_items;
    }

  } /* namespace lora */
} /* namespace gr */