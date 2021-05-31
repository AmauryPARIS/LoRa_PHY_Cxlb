#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "gray_enc_impl.h"

namespace gr {
  namespace lora_sdr {

    gray_enc::sptr
    gray_enc::make( )
    {
      return gnuradio::get_initial_sptr
        (new gray_enc_impl());
    }

    /*
     * The private constructor
     */
    gray_enc_impl::gray_enc_impl( )
      : gr::sync_block("gray_enc",
            gr::io_signature::make(1, 1, sizeof(uint32_t)),
            gr::io_signature::make(1, 1, sizeof(uint32_t)))
    {}

    /*
     * Our virtual destructor.
     */
    gray_enc_impl::~gray_enc_impl()
    {}

    int gray_enc_impl::work(int noutput_items,
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
        }

        for(int i=0; i<noutput_items;i++){
            out[i]= (in[i] ^ (in[i] >> 1u));
            #ifdef GRLORA_DEBUG
            std::cout<<std::hex<<"0x"<<in[i]<<" ---> "<<"0x"<<out[i]<<std::dec<<std::endl;
            #endif
        }
        // std::cout << "gray len : " << (int)(out[0]<<4)+out[1] <<  "\n";
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
