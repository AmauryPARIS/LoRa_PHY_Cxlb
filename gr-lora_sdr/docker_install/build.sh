#!/bin/bash
# Build and source script for LoRa physical layer

# Source the path to lora_sdr
. /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/setpaths.sh
# And copy it to .bashrc so that it stays sourced
cat /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/setpaths.sh >> /root/.bashrc 

# Matthieu's path
. /cortexlab/toolchains/current/bin/cxlb-toolchain-user-conf

# ------------------------------------------------------------------------
# Build

cd /root/LoRa_PHY_Cxlb.git/gr-lora_sdr
mkdir build
cd /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/build
cmake ../
make
make install

# ------------------------------------------------------------------------
# Load the blocks in GRC
mkdir /root/.gnuradio
echo "\
[grc]
local_blocks_path=/root/LoRa_PHY_Cxlb.git/gr-lora_sdr/grc\
" > /root/.gnuradio/config.conf

# ------------------------------------------------------------------------
# Build hierarchical blocks
grc_build_block() {
    # build a gnuradio-companion hierarchical block
    # param 1: grc filename
    GRC="$1"
    STEM=${GRC%.grc}
    echo "### build grc hier block $GRC"
    echo "### set environment"
    eval "$SET_TOOLCHAIN_ENV"
    echo "### grc compilation"
    COUNT=1

    until echo "### try $COUNT" && grcc -d . $STEM.grc || [ "$COUNT" -ge 20 ] ; do
        COUNT=$((COUNT+1))
    done
    # compilation retried several times because grcc randomly fails since I added thrift libs for ctrlport :-/

    # WARN: currently option -d does not work -> compiled .py and
    # .py.xml go in ~/.grc_gnuradio, hence the following hack
    
    # echo "### bad grc compilation output directory hack"
    # cp ~/.grc_gnuradio/$STEM.py ~/.grc_gnuradio/$STEM.py.xml .


    # the following hack to fix what seems to be a strange bug of
    # grcc, which occurs only in some circumstances, where the python
    # imports are not correct

    # echo "### fix compiled grc imports"
    # xalan -xsl $SCRIPTLOCATION/fix_xml.xsl -param pythondir "'$TC_PYTHONPATH'" -param modulename "'$STEM'" < $STEM.py.xml > $STEM.py.xml.tmp
    # mv $STEM.py.xml.tmp $STEM.py.xml

    # echo "### install compiled grc .py and xml in gnuradio"
    # cp $STEM.py "$TC_PYTHONPATH"
    # cp $STEM.py.xml $INSTALL_DIR/share/gnuradio/grc/blocks/
}

cd /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/Hier\ blocks/
ls
grc_build_block hier_rx.grc
grc_build_block hier_tx.grc

