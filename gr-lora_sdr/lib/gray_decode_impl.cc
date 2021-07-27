#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "gray_decode_impl.h"
#include <lora_sdr/utilities.h>

namespace gr {
  namespace lora_sdr {

    gray_decode::sptr
    gray_decode::make(uint8_t sf)
    {
      return gnuradio::get_initial_sptr
        (new gray_decode_impl(sf));
    }
    /*
     * The private constructor
     */
    gray_decode_impl::gray_decode_impl(uint8_t sf)
      : gr::sync_block("gray_decode",
              gr::io_signature::make(1, 1, sizeof(uint32_t)),
              gr::io_signature::make(1, 1, sizeof(uint32_t)))
    {
        m_sf=sf;
    }

    /*
     * Our virtual destructor.
     */
    gray_decode_impl::~gray_decode_impl()
    {}

    int
    gray_decode_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const uint32_t *in = (const uint32_t *) input_items[0];
      uint32_t *out = (uint32_t *) output_items[0];

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
          if (key == "SF"){
            m_sf = value;
            // std::cout << "Interleaver imp - New SF : " << value << "\n";
          } 
        }
      }

      for(int i=0;i<noutput_items;i++){
        #ifdef GRLORA_DEBUG
        std::cout<<std::hex<<"0x"<<in[i]<<" -->  ";
        #endif
        out[i]=in[i];
        for(int j=1;j<m_sf;j++){
             out[i]=out[i]^(in[i]>>j);
        }
        //do the shift of 1
         out[i]=mod(out[i]+1,(1<<m_sf));
         #ifdef GRLORA_DEBUG
         std::cout<<"0x"<<out[i]<<std::dec<<std::endl;
         #endif
      }

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
