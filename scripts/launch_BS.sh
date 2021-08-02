#!/bin/bash
source /cortexlab/toolchains/current/bin/cxlb-toolchain-user-conf
# Source the path to lora_sdr
. /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/setpaths.sh
# And copy it to .bashrc so that it stays sourced
cat /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/setpaths.sh >> /root/.bashrc
python2 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/lora_dyn_node.py "$@" | tee ./phy_BS.log 2>&1 &
sleep 5
python3 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/advanced_test/automate/udp_BS_less_param.py | tee ./up_BS.log 2>&1
