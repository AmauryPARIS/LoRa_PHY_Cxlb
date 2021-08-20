#!/bin/bash
. /cortexlab/toolchains/current/bin/cxlb-toolchain-user-conf
# Source the path to lora_sdr
. /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/setpaths.sh
# And copy it to .bashrc so that it stays sourced
cat /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/setpaths.sh >> /root/.bashrc
env > /root/launch_node_env
sleep 5
ARG1="$1"
ARG2="$2"
ARG3="$3"
ARG4="$4"
shift 4
/root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/lora_dyn_node.py "$@" 2>&1 | tee ./phy_node.log &
sleep 7
python3 /root/LoRa_PHY_Cxlb.git/gr-lora_sdr/apps/advanced_test/automate/udp_node_less_param.py "$ARG1" "$ARG2" "$ARG3" "$ARG4" "$@" 2>&1 | tee ./up_node.log 
